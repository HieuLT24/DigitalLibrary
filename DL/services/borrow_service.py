from datetime import date, timedelta
from DL.models import db, Book, BorrowRequest, BorrowSlip

class BorrowService:
    # ------------------ Helpers ------------------
    def get_book(self, book_id):
        return Book.query.get(book_id)

    def user_is_borrowing(self, user_id, book_id):
        return db.session.query(BorrowSlip.slip_id).filter(
            BorrowSlip.user_id == user_id,
            BorrowSlip.book_id == book_id,
            BorrowSlip.status == "borrowed"
        ).first() is not None

    def get_existing_active_request(self, user_id, book_id):
        return BorrowRequest.query.filter(
            BorrowRequest.user_id == user_id,
            BorrowRequest.book_id == book_id,
            BorrowRequest.status.in_(["pending", "approved"])
        ).first()

    # ------------------ Allocation ------------------
    def get_book_allocation(self, book_id):
        borrowed_count = BorrowSlip.query.filter(
            BorrowSlip.book_id == book_id,
            BorrowSlip.status == "borrowed"
        ).count()
        approved_count = BorrowRequest.query.filter(
            BorrowRequest.book_id == book_id,
            BorrowRequest.status == "approved"
        ).count()
        return borrowed_count, approved_count

    def can_approve_more(self, book: Book):
        if book.quantity is None:
            return True
        borrowed_count, approved_count = self.get_book_allocation(book.book_id)
        allocated = borrowed_count + approved_count
        return allocated < book.quantity

    # ------------------ NEW: cập nhật trạng thái sách ------------------
    def update_book_status(self, book: Book):
        """
        Điều chỉnh tuỳ theo logic bạn muốn. Ở đây:
        - Nếu quantity is None => always available
        - Nếu quantity > 0 => available, else out_of_stock
        """
        if not hasattr(book, 'status'):
            return
        if book.quantity is None:
            book.status = 'available'
        else:
            book.status = 'available' if book.quantity > 0 else 'out_of_stock'

    # ------------------ User: tạo request ------------------
    def create_request(self, user_id, book_id):
        book = self.get_book(book_id)
        if not book:
            raise ValueError("BOOK_NOT_FOUND")
        if book.quantity is not None and book.quantity <= 0:
            raise ValueError("OUT_OF_STOCK")
        if self.user_is_borrowing(user_id, book_id):
            raise ValueError("ALREADY_BORROWING")
        if self.get_existing_active_request(user_id, book_id):
            raise ValueError("REQUEST_ALREADY_EXISTS")
        req = BorrowRequest(
            request_date=date.today(),
            status="pending",
            user_id=user_id,
            book_id=book_id
        )
        db.session.add(req)
        db.session.commit()
        return req

    # ------------------ UI state ------------------
    def get_user_state_for_book(self, user_id, book_id):
        state = {
            "is_borrowing": self.user_is_borrowing(user_id, book_id),
            "request_status": None,
            "request_id": None
        }
        req = self.get_existing_active_request(user_id, book_id)
        if req:
            state["request_status"] = req.status
            state["request_id"] = req.request_id
        return state

    # ------------------ Overview user loans ------------------
    def get_user_overview(self, user_id):
        borrowed = (BorrowSlip.query
                    .filter_by(user_id=user_id, status="borrowed")
                    .join(Book)
                    .order_by(BorrowSlip.slip_id.desc())
                    .all())

        pending = (BorrowRequest.query
                   .filter_by(user_id=user_id, status="pending")
                   .join(Book)
                   .order_by(BorrowRequest.request_id.desc())
                   .all())

        approved = (BorrowRequest.query
                    .filter_by(user_id=user_id, status="approved")
                    .join(Book)
                    .order_by(BorrowRequest.request_id.desc())
                    .all())

        canceled = (BorrowRequest.query
                    .filter_by(user_id=user_id, status="canceled")
                    .join(Book)
                    .order_by(BorrowRequest.request_id.desc())
                    .all())

        rejected = (BorrowRequest.query
                    .filter_by(user_id=user_id, status="rejected")
                    .join(Book)
                    .order_by(BorrowRequest.request_id.desc())
                    .all())

        return {
            "borrowed": borrowed,
            "pending": pending,
            "approved": approved,
            "canceled": canceled,
            "rejected": rejected
        }

    # ------------------ User cancel ------------------
    def cancel_request(self, user_id, request_id):
        req = BorrowRequest.query.filter_by(request_id=request_id, user_id=user_id).first()
        if not req:
            raise ValueError("REQUEST_NOT_FOUND")
        if req.status != "pending":
            # Nếu muốn cho hủy cả approved: thay bằng
            # if req.status not in ("pending","approved"):
            raise ValueError("CANNOT_CANCEL")
        req.status = "canceled"
        db.session.commit()
        return req

    # ------------------ Admin approve ------------------
    def approve_request(self, request_id):
        req = BorrowRequest.query.get(request_id)
        if not req:
            raise ValueError("REQUEST_NOT_FOUND")
        if req.status != "pending":
            raise ValueError("INVALID_STATE")
        book = self.get_book(req.book_id)
        if not book:
            raise ValueError("BOOK_NOT_FOUND")
        if not self.can_approve_more(book):
            raise ValueError("NO_AVAILABLE_QUANTITY")
        req.status = "approved"
        db.session.commit()
        return req

    # ------------------ Admin convert (giao) ------------------
    def convert_request_to_slip(self, request_id, loan_days=14):
        req = BorrowRequest.query.get(request_id)
        if not req:
            raise ValueError("REQUEST_NOT_FOUND")
        if req.status != "approved":
            raise ValueError("INVALID_STATE")
        book = self.get_book(req.book_id)
        if not book:
            raise ValueError("BOOK_NOT_FOUND")
        if book.quantity is not None and book.quantity <= 0:
            raise ValueError("OUT_OF_STOCK")

        slip = BorrowSlip(
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=loan_days),
            status="borrowed",
            user_id=req.user_id,
            book_id=req.book_id
        )
        if book.quantity is not None:
            book.quantity -= 1
        self.update_book_status(book)

        req.status = "converted"
        db.session.add(slip)
        db.session.commit()
        return slip

    # ------------------ Admin reject ------------------
    def reject_request(self, request_id, reason=None):
        req = BorrowRequest.query.get(request_id)
        if not req:
            raise ValueError("REQUEST_NOT_FOUND")
        if req.status != "pending":
            raise ValueError("INVALID_STATE")
        req.status = "rejected"
        req.reject_reason = reason or "Từ chối"
        db.session.commit()
        return req

    # ------------------ Listing requests ------------------
    def get_user_requests(self, user_id, statuses=None, include_canceled=False):
        q = BorrowRequest.query.filter(BorrowRequest.user_id == user_id)
        if statuses:
            q = q.filter(BorrowRequest.status.in_(statuses))
        else:
            if not include_canceled:
                q = q.filter(BorrowRequest.status != "canceled")
        return q.order_by(BorrowRequest.request_id.desc()).all()

    def list_requests(self, statuses=None):
        q = BorrowRequest.query
        if statuses:
            q = q.filter(BorrowRequest.status.in_(statuses))
        return q.order_by(BorrowRequest.request_id.desc()).all()

    # ------------------ NEW: Borrow history ------------------
    def get_borrow_history(self, user_id, statuses=None):
        q = BorrowSlip.query.filter(BorrowSlip.user_id == user_id)
        if statuses:
            q = q.filter(BorrowSlip.status.in_(statuses))
        return (q.join(Book)
                 .order_by(
                     db.case((BorrowSlip.status == 'borrowed', 0), else_=1),
                     BorrowSlip.borrow_date.desc()
                 ).all())

    # ------------------ NEW: Return book ------------------
    def return_book(self, slip_id):
        slip = BorrowSlip.query.get(slip_id)
        if not slip:
            raise ValueError("SLIP_NOT_FOUND")
        if slip.status != "borrowed":
            raise ValueError("INVALID_STATE")
        book = self.get_book(slip.book_id)
        slip.status = "returned"
        slip.return_date = date.today()
        if book and book.quantity is not None:
            book.quantity += 1
            self.update_book_status(book)
        db.session.commit()
        return slip

    # ------------------ NEW: Lost / Damaged ------------------
    def mark_lost(self, slip_id):
        slip = BorrowSlip.query.get(slip_id)
        if not slip:
            raise ValueError("SLIP_NOT_FOUND")
        if slip.status != "borrowed":
            raise ValueError("INVALID_STATE")
        slip.status = "lost"
        slip.return_date = date.today()
        book = self.get_book(slip.book_id)
        if book:
            self.update_book_status(book)
        db.session.commit()
        return slip

    def mark_damaged(self, slip_id):
        slip = BorrowSlip.query.get(slip_id)
        if not slip:
            raise ValueError("SLIP_NOT_FOUND")
        if slip.status != "borrowed":
            raise ValueError("INVALID_STATE")
        slip.status = "damaged"
        slip.return_date = date.today()
        book = self.get_book(slip.book_id)
        if book:
            self.update_book_status(book)
        db.session.commit()
        return slip
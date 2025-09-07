from datetime import date
from DL.models import db, Book, BorrowRequest, BorrowSlip

class BorrowService:
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

    def get_user_overview(self, user_id):
        """
        Trả về dict gồm 3 lists:
        {
          borrowed: [BorrowSlip ...],
          pending: [BorrowRequest ...],
          approved: [BorrowRequest ...]
        }
        """
        borrowed = BorrowSlip.query.filter_by(user_id=user_id, status="borrowed") \
                                   .join(Book).order_by(BorrowSlip.slip_id.desc()).all()
        pending = BorrowRequest.query.filter_by(user_id=user_id, status="pending") \
                                     .join(Book).order_by(BorrowRequest.request_id.desc()).all()
        approved = BorrowRequest.query.filter_by(user_id=user_id, status="approved") \
                                      .join(Book).order_by(BorrowRequest.request_id.desc()).all()
        return {
            "borrowed": borrowed,
            "pending": pending,
            "approved": approved
        }

    def cancel_request(self, user_id, request_id):
        req = BorrowRequest.query.filter_by(request_id=request_id, user_id=user_id).first()
        if not req:
            raise ValueError("REQUEST_NOT_FOUND")
        if req.status != "pending":
            raise ValueError("CANNOT_CANCEL")
        req.status = "canceled"
        db.session.commit()
        return req
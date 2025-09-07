from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required, current_user

from DL.models import db, Book, BorrowSlip, User, Category, BorrowRequest
from DL.services.borrow_service import BorrowService

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/")
@login_required
def admin_index():
    if current_user.role != 'admin':
        return abort(403)

    total_books = db.session.query(Book).count()
    borrowing_books = db.session.query(BorrowSlip).filter(BorrowSlip.status == 'borrowed').count()
    total_users = db.session.query(User).count()
    total_borrows = db.session.query(BorrowSlip).count()

    category_counts = (
        db.session.query(Category.name, db.func.count(Book.book_id))
        .join(Book, Book.category_id == Category.category_id)
        .group_by(Category.category_id, Category.name)
        .all()
    )
    books_by_category_labels = [name or 'Không xác định' for name, _ in category_counts]
    books_by_category_counts = [cnt for _, cnt in category_counts]

    borrow_counts_by_library = (
        db.session.query(Book.library_location, db.func.count(BorrowSlip.slip_id))
        .join(BorrowSlip, BorrowSlip.book_id == Book.book_id)
        .group_by(Book.library_location)
        .all()
    )

    stats = {
        'total_books': total_books,
        'borrowing_books': borrowing_books,
        'total_users': total_users,
        'total_borrows': total_borrows,
        'books_by_category_labels': books_by_category_labels,
        'books_by_category_counts': books_by_category_counts,
        'borrow_counts_by_library': [
            {'library_location': lib, 'borrow_count': cnt} for lib, cnt in borrow_counts_by_library
        ],
    }
    return render_template("admin_templates/statistic.html", stats=stats)

@admin_bp.route("/requests")
@login_required
def admin_requests():
    if current_user.role != 'admin':
        return abort(403)

    status_filter = request.args.get('status')  # có thể None = all
    service = BorrowService()

    allowed = ['pending', 'approved', 'rejected', 'converted']
    if status_filter in allowed:
        requests = service.list_requests(statuses=[status_filter])
    else:
        requests = service.list_requests()

    counts = {st: db.session.query(BorrowRequest).filter(BorrowRequest.status == st).count()
              for st in allowed}

    return render_template("admin_templates/admin_requests.html",
                           requests=requests,
                           counts=counts,
                           current_filter=status_filter)

@admin_bp.route("/requests/<int:request_id>/approve", methods=['POST'])
@login_required
def approve_request(request_id):
    if current_user.role != 'admin':
        return abort(403)
    service = BorrowService()
    try:
        service.approve_request(request_id)
        flash("Đã duyệt yêu cầu.", "success")
    except ValueError as e:
        mapping = {
            "REQUEST_NOT_FOUND": "Không tìm thấy yêu cầu.",
            "INVALID_STATE": "Trạng thái không hợp lệ.",
            "BOOK_NOT_FOUND": "Không tìm thấy sách.",
            "NO_AVAILABLE_QUANTITY": "Không còn suất để duyệt (đã đủ số lượng)."
        }
        flash(mapping.get(str(e), "Duyệt thất bại."), "danger")
    return redirect(url_for('admin.admin_requests', status='pending'))

@admin_bp.route("/requests/<int:request_id>/convert", methods=['POST'])
@login_required
def convert_request(request_id):
    if current_user.role != 'admin':
        return abort(403)
    service = BorrowService()
    try:
        service.convert_request_to_slip(request_id)
        flash("Đã tạo phiếu mượn (giao sách).", "success")
    except ValueError as e:
        mapping = {
            "REQUEST_NOT_FOUND": "Không tìm thấy yêu cầu.",
            "INVALID_STATE": "Yêu cầu không ở trạng thái đã duyệt.",
            "BOOK_NOT_FOUND": "Không tìm thấy sách.",
            "OUT_OF_STOCK": "Sách đã hết khi giao."
        }
        flash(mapping.get(str(e), "Tạo phiếu thất bại."), "danger")
    return redirect(url_for('admin.admin_requests', status='approved'))

@admin_bp.route("/requests/<int:request_id>/reject", methods=['POST'])
@login_required
def reject_request(request_id):
    if current_user.role != 'admin':
        return abort(403)
    service = BorrowService()
    reason = request.form.get('reject_reason') or None
    try:
        service.reject_request(request_id, reason)
        flash("Đã từ chối yêu cầu.", "info")
    except ValueError as e:
        mapping = {
            "REQUEST_NOT_FOUND": "Không tìm thấy yêu cầu.",
            "INVALID_STATE": "Trạng thái không hợp lệ."
        }
        flash(mapping.get(str(e), "Từ chối thất bại."), "danger")
    return redirect(url_for('admin.admin_requests', status='pending'))

@admin_bp.route("/add-book")
@login_required
def add_book():
    if current_user.role != 'admin':
        return abort(403)
    return render_template("admin_templates/add_book.html")
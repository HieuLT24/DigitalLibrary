from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date, timedelta

from DL.models import db, Book, BorrowSlip, User, Category, BorrowRequest
from sqlalchemy.orm import joinedload

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/")
@login_required
def admin_index():
    if current_user.role != 'admin':
        return abort(403)

    total_books = db.session.query(Book).count()
    borrowing_books = db.session.query(BorrowSlip).filter(BorrowSlip.status == 'borrowing').count()
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
            { 'library_location': lib, 'borrow_count': cnt } for lib, cnt in borrow_counts_by_library
        ],
    }

    return render_template("admin_templates/statistic.html", stats=stats)

@admin_bp.route("/requests")
@login_required
def admin_requests():
    if current_user.role != 'admin':
        return abort(403)
    
    status_filter = request.args.get('status', 'pending')
    
    query = db.session.query(BorrowRequest).options(
        db.joinedload(BorrowRequest.user),
        db.joinedload(BorrowRequest.book)
    )
    
    if status_filter in ['pending', 'approved', 'rejected']:
        query = query.filter(BorrowRequest.status == status_filter)
    
    borrow_requests = query.all()
    
    pending_count = db.session.query(BorrowRequest).filter(BorrowRequest.status == 'pending').count()
    approved_count = db.session.query(BorrowRequest).filter(BorrowRequest.status == 'approved').count()
    rejected_count = db.session.query(BorrowRequest).filter(BorrowRequest.status == 'rejected').count()
    
    stats = {
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    }
    
    return render_template("admin_templates/admin_requests.html",  
                         requests=borrow_requests, stats=stats, current_filter=status_filter)


@admin_bp.route("/requests/<int:request_id>/approve", methods=['POST'])
@login_required
def approve_request(request_id):
    if current_user.role != 'admin':
        return abort(403)
    
    borrow_request = BorrowRequest.query.get_or_404(request_id)
    
    if borrow_request.status == 'pending':
        borrow_request.status = 'approved'
        
        borrow_slip = BorrowSlip(
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=14),
            status='borrowing',
            user_id=borrow_request.user_id,
            book_id=borrow_request.book_id
        )
        
        db.session.add(borrow_slip)
        db.session.commit()
        
        flash('Đã duyệt yêu cầu mượn sách thành công!', 'success')
    else:
        flash('Yêu cầu này đã được xử lý trước đó.', 'warning')
    
    return redirect(url_for('admin.admin_requests', status='pending'))

@admin_bp.route("/requests/<int:request_id>/reject", methods=['POST'])
@login_required
def reject_request(request_id):
    if current_user.role != 'admin':
        return abort(403)
    
    borrow_request = BorrowRequest.query.get_or_404(request_id)
    reject_reason = request.form.get('reject_reason', '')
    
    if borrow_request.status == 'pending':
        borrow_request.status = 'rejected'
        borrow_request.reject_reason = reject_reason
        
        db.session.commit()
        
        flash('Đã từ chối yêu cầu mượn sách.', 'info')
    else:
        flash('Yêu cầu này đã được xử lý trước đó.', 'warning')
    
    return redirect(url_for('admin.admin_requests', status='pending'))

@admin_bp.route("/add-book")
def add_book():
    return render_template("admin_templates/add_book.html")
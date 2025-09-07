from flask import Blueprint, render_template, request, abort, flash, redirect, url_for
from flask_login import current_user, login_required

from DL.models import Book, db
from DL.services.book_service import BookService
from DL.services.borrow_service import BorrowService

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    service = BookService()
    random_books = service.get_random_books(limit=4)
    return render_template("index.html", random_books=random_books)

@main_bp.route("/books")
def book_list():
    page = request.args.get("page", 1, type=int)
    per_page = 8
    service = BookService()
    pagination = service.get_paginated_books(page=page, per_page=per_page, order_desc=True)
    books = pagination.items
    return render_template("book_list.html", books=books, pagination=pagination)

@main_bp.route("/book/<int:book_id>")
def book_detail(book_id):
    book_service = BookService()
    borrow_service = BorrowService()
    book = book_service.get_book_by_id(book_id)
    if not book:
        abort(404)
    user_state = None
    if current_user.is_authenticated:
        user_state = borrow_service.get_user_state_for_book(current_user.user_id, book_id)
    return render_template("book_detail.html", book=book, user_state=user_state)

@main_bp.route("/book/<int:book_id>/request-borrow", methods=["POST"])
@login_required
def request_borrow(book_id):
    borrow_service = BorrowService()
    try:
        borrow_service.create_request(current_user.user_id, book_id)
        flash("Gửi yêu cầu mượn thành công. Vui lòng chờ phê duyệt.", "success")
    except ValueError as e:
        code = str(e)
        msg_map = {
            "BOOK_NOT_FOUND": "Không tìm thấy sách.",
            "OUT_OF_STOCK": "Sách đã hết.",
            "ALREADY_BORROWING": "Bạn đang mượn sách này.",
            "REQUEST_ALREADY_EXISTS": "Bạn đã có yêu cầu đang chờ / đã duyệt."
        }
        flash(msg_map.get(code, "Không thể gửi yêu cầu."), "danger")
    return redirect(url_for('main.book_detail', book_id=book_id))
@main_bp.route("/search")
def search():
    search_query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 16, type=int)
    service = BookService()
    pagination = service.search_books(keyword=search_query, page=page, per_page=per_page)
    return render_template("search.html", search_query=search_query, pagination=pagination, books=pagination.items)


@main_bp.route("/search/quick")
def search_quick():
    """Trả về HTML nhỏ (partial) gồm tối đa 5 sách phù hợp để hiển thị dropdown nhanh."""
    keyword = request.args.get('q', '').strip()
    limit = request.args.get('limit', 5, type=int)
    service = BookService()
    pagination = service.search_books(keyword=keyword, page=1, per_page=limit)
    books = pagination.items if pagination else []
    return render_template("partials/quick_search_items.html", books=books)


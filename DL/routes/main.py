from flask import Blueprint, render_template, request, abort

from DL.models import Book, db
from DL.services.book_service import BookService

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
    service = BookService()
    book = service.get_book_by_id(book_id)
    if not book:
        abort(404)
    return render_template("book_detail.html", book=book)

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


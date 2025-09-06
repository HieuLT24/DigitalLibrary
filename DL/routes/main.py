from flask import Blueprint, render_template, request, abort

from DL.models import Book

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/books")
def book_list():
    page = request.args.get("page", 1, type=int)
    per_page = 8
    pagination = Book.query.order_by(Book.book_id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    books = pagination.items
    return render_template("book_list.html", books=books, pagination=pagination)

@main_bp.route("/book/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404)
    return render_template("book_detail.html", book=book)
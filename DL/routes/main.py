from flask import Blueprint, render_template, request, abort

from DL.models import Book, db

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    random_books = Book.query.order_by(db.func.random()).limit(4).all()
    return render_template("index.html", random_books=random_books)

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

@main_bp.route("/search")
def search():
    search_query = request.args.get('q', '')
    return render_template("search.html", search_query=search_query, total_results=0)


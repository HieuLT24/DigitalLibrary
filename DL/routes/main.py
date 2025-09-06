from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/book/<int:book_id>")
def book_detail(book_id):
    sample_book = {
        "id": book_id,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "978-0-7432-7356-5",
        "genre": "Tiểu thuyết",
        "description": "Một trong những tác phẩm kinh điển nhất của văn học Mỹ..."
    }
    return render_template("book_detail.html", book=sample_book)

@main_bp.route("/search")
def search():
    search_query = request.args.get('q', '')
    return render_template("search.html", search_query=search_query, total_results=0)

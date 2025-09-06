from flask import Blueprint, request, jsonify
from DL.models import Book, Author, Category, db
from DL.services.book_service import BookService

book_controller = Blueprint('book_controller', __name__)
book_service = BookService()

@book_controller.route("/api/books", methods=['GET'])
def get_all_books():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        result = book_service.get_all_books(page, per_page)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500

@book_controller.route("/api/books/search", methods=['GET'])
def search_books():
    try:
        keyword = request.args.get('q', '').strip()
        category_id = request.args.get('category_id', type=int)
        author_id = request.args.get('author_id', type=int)
        status = request.args.get('status', 'available')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        result = book_service.search_books(
            keyword=keyword,
            category_id=category_id,
            author_id=author_id,
            status=status,
            page=page,
            per_page=per_page
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi khi tìm kiếm: {str(e)}'
        }), 500

@book_controller.route("/api/books/<int:book_id>", methods=['GET'])
def get_book_by_id(book_id):
    try:
        result = book_service.get_book_by_id(book_id)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500


@book_controller.route("/api/categories", methods=['GET'])
def get_categories():
    try:
        result = book_service.get_categories()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500

@book_controller.route("/api/authors", methods=['GET'])
def get_authors():
    try:
        result = book_service.get_authors()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500

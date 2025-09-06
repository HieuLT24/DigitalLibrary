from flask import Blueprint, request, jsonify
from DL.models import Book, Author, Category, db
from DL.services.book_service import BookService

book_controller = Blueprint('book_controller', __name__)
book_service = BookService()

@book_controller.route("/books", methods=['GET'])
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

@book_controller.route("/books/search", methods=['GET'])
def search_books():
    try:
        keyword = request.args.get('q', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 9, type=int)
        
        result = book_service.search_books(
            keyword=keyword,
            page=page,
            per_page=per_page
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi khi tìm kiếm: {str(e)}'
        }), 500

@book_controller.route("/books/<int:book_id>", methods=['GET'])
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


@book_controller.route("/categories", methods=['GET'])
def get_categories():
    try:
        result = book_service.get_categories()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500

@book_controller.route("/authors", methods=['GET'])
def get_authors():
    try:
        result = book_service.get_authors()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500

@book_controller.route("/api/books/random", methods=['GET'])
def random_books():
    try:
        limit = request.args.get('limit', 4, type=int)
        result = book_service.get_random_books(limit=limit)
        return jsonify(result), (200 if result['success'] else 500)
    except Exception as e:
        return jsonify({'success': False,'message': f'Lỗi: {str(e)}'}), 500
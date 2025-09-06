from DL.models import Book, Author, Category, db

class BookService:
    
    def get_all_books(self, page=1, per_page=10):
        try:
            pagination = Book.query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            
            books = []
            for book in pagination.items:
                books.append(book.to_dict())
            
            return {
                'success': True,
                'data': {
                    'books': books,
                    'pagination': {
                        'page': pagination.page,
                        'pages': pagination.pages,
                        'per_page': pagination.per_page,
                        'total': pagination.total
                    }
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi khi lấy danh sách sách: {str(e)}'
            }
    
    def search_books(self, keyword='', category_id=None, author_id=None, 
                    status='available', page=1, per_page=10):
        try:
            query = Book.query
            
            if keyword:
                query = query.filter(
                    db.or_(
                        Book.title.contains(keyword),
                        Book.description.contains(keyword),
                        Book.isbn.contains(keyword)
                    )
                )
            if category_id:
                query = query.filter(Book.category_id == category_id)
            
            if author_id:
                query = query.filter(Book.author_id == author_id)

            if status:
                query = query.filter(Book.status == status)
            
            pagination = query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            
            books = []
            for book in pagination.items:
                books.append(book.to_dict())
            
            return {
                'success': True,
                'data': {
                    'books': books,
                    'pagination': {
                        'page': pagination.page,
                        'pages': pagination.pages,
                        'per_page': pagination.per_page,
                        'total': pagination.total,
                        'has_next': pagination.has_next,
                        'has_prev': pagination.has_prev
                    }
                },
                'message': f'Tìm thấy {pagination.total} sách'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi khi tìm kiếm: {str(e)}'
            }
    
    def get_book_by_id(self, book_id):
        try:
            book = Book.query.get(book_id)
            
            if not book:
                return {
                    'success': False,
                    'message': f'Không tìm thấy sách với ID {book_id}'
                }
            
            return {
                'success': True,
                'data': book.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi: {str(e)}'
            }
    
    
    
    def get_categories(self):
        try:
            categories = Category.query.all()
            categories_data = []
            
            for category in categories:
                categories_data.append(category.to_dict())
            
            return {
                'success': True,
                'data': categories_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi khi lấy danh mục: {str(e)}'
            }
    
    def get_authors(self):
        try:
            authors = Author.query.all()
            authors_data = []
            
            for author in authors:
                authors_data.append(author.to_dict())
            
            return {
                'success': True,
                'data': authors_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi khi lấy tác giả: {str(e)}'
            }

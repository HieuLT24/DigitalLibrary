from DL.models import Book, Author, Category, db

class BookService:
    
    def get_random_books(self, limit=4):
        return Book.query.order_by(db.func.rand()).limit(limit).all()

    def get_paginated_books(self, page=1, per_page=10, order_desc=True):
        query = Book.query
        if order_desc:
            query = query.order_by(Book.book_id.desc())
        return query.paginate(page=page, per_page=per_page, error_out=False)

    def get_book_by_id(self, book_id):
        return Book.query.get(book_id)

    def search_books(self, keyword='', page=1, per_page=16):
        query = Book.query
        if keyword:
            query = query.filter(
                db.or_(
                    Book.title.contains(keyword),
                    Book.description.contains(keyword),
                    Book.isbn.contains(keyword)
                )
            )
        return query.paginate(page=page, per_page=per_page, error_out=False)

    
    def get_categories(self):
        return Category.query.all()
    
    def get_authors(self):
        return Author.query.all()

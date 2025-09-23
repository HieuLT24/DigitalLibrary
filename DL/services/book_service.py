from DL.models import Book, Author, Category, db
import cloudinary.uploader

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

    def search_books(self, keyword='', filters=None, page=1, per_page=16):
        query = Book.query.join(Author).join(Category)
        
        if keyword:
            query = query.filter(
                db.or_(
                    Book.title.contains(keyword),
                    Book.description.contains(keyword),
                    Book.isbn.contains(keyword),
                    Author.name.contains(keyword),
                    Category.name.contains(keyword)
                )
            )
        
        if filters:
            if 'library' in filters and filters['library']:
                query = query.filter(Book.library_location == filters['library'])
            
            if 'category' in filters and filters['category']:
                if isinstance(filters['category'], int):
                    query = query.filter(Book.category_id == filters['category'])
                else:
                    query = query.filter(Category.name.contains(filters['category']))
            
            if 'author' in filters and filters['author']:
                if isinstance(filters['author'], int):
                    query = query.filter(Book.author_id == filters['author'])
                else:
                    query = query.filter(Author.name.contains(filters['author']))
            
            if 'language' in filters and filters['language']:
                query = query.filter(Book.language == filters['language'])
            
            if 'status' in filters and filters['status']:
                query = query.filter(Book.status == filters['status'])
        
        return query.paginate(page=page, per_page=per_page, error_out=False)

    
    def get_categories(self):
        return Category.query.all()
    
    def get_authors(self):
        return Author.query.all()
    
    def get_filter_options(self):
        categories = [{'category_id': c.category_id, 'name': c.name} for c in Category.query.all()]
        authors = [{'author_id': a.author_id, 'name': a.name} for a in Author.query.all()]
        
        libraries = db.session.query(Book.library_location).distinct().filter(Book.library_location.isnot(None)).all()
        libraries = [lib[0] for lib in libraries if lib[0]]
        
        return {
            'categories': categories,
            'authors': authors,
            'libraries': libraries
        }
    
    def add_book(self, data, image_file=None):
        """Thêm sách mới vào DB, kèm upload ảnh lên Cloudinary."""
        image_url = None

        if image_file:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder="library/books"
            )
            image_url = upload_result.get("secure_url")

        new_book = Book(
            title=data.get("title"),
            publisher=data.get("publisher"),
            category_id=data.get("category_id"),
            isbn=data.get("isbn"),
            language=data.get("language"),
            publish_year=data.get("publish_year"),
            quantity=int(data.get("quantity")) if data.get("quantity") else 1,
            description=data.get("description"),
            library_location=data.get("library_location", "Kho chính"),
            image=image_url,
            author_id=data.get("author_id"),
            status="available"
        )

        db.session.add(new_book)
        db.session.commit()
        return new_book



from . import db

class Book(db.Model):
    __tablename__ = "book"
    
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    publisher = db.Column(db.String(100))
    publish_year = db.Column(db.String(10))
    language = db.Column(db.String(50))
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=1)
    library_location = db.Column(db.String(100))
    

    weight = db.Column(db.Float)
    size = db.Column(db.String(100))
    page_count = db.Column(db.Integer)
    cover_type = db.Column(db.String(100))
    isbn = db.Column(db.String(100))
    image = db.Column(db.String(255))
    status = db.Column(db.String(50), default="available")

    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.author_id"), nullable=False)
    
    borrow_slips = db.relationship("BorrowSlip", backref="book", lazy=True)

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "publisher": self.publisher,
            "publish_year": self.publish_year,
            "language": self.language,
            "description": self.description,
            "quantity": self.quantity,
            "library_location": self.library_location,
            "weight": self.weight,
            "size": self.size,
            "page_count": self.page_count,
            "cover_type": self.cover_type,
            "isbn": self.isbn,
            "image": self.image,
            "status": self.status,
            "category_id": self.category_id,
            "author_id": self.author_id,
            "author_name": self.author.name if self.author else None,
            "category_name": self.category.name if self.category else None
        }

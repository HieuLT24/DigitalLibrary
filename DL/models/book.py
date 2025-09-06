

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
    status = db.Column(db.String(50), default="available")

    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.author_id"), nullable=False)
    
    borrow_slips = db.relationship("BorrowSlip", backref="book", lazy=True)

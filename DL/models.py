from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="active")

    borrow_requests = db.relationship("BorrowRequest", backref="user", lazy=True)
    borrow_slips = db.relationship("BorrowSlip", backref="user", lazy=True)
    notifications = db.relationship("Notification", backref="user", lazy=True)
    reports = db.relationship("Report", backref="user", lazy=True)


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

class Author(db.Model):
    __tablename__ = "author"
    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    
    books = db.relationship("Book", backref="author", lazy=True)

class Category(db.Model):
    __tablename__ = "category"
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    books = db.relationship("Book", backref="category", lazy=True)


class BorrowSlip(db.Model):
    __tablename__ = "borrow_slip"
    slip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    borrow_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    status = db.Column(db.String(50))


    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id"), nullable=False)


class BorrowRequest(db.Model):
    __tablename__ = "borrow_request"
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50))
    reject_reason = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)


class Notification(db.Model):
    __tablename__ = "notification"
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    sent_date = db.Column(db.Date)
    type = db.Column(db.String(50))


    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
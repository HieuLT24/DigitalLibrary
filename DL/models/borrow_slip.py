

from . import db

class BorrowSlip(db.Model):
    __tablename__ = "borrow_slip"
    
    slip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    borrow_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    status = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id"), nullable=False)
    



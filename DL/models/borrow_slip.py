

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
    
    def to_dict(self):
        return {
            'slip_id': self.slip_id,
            'borrow_date': self.borrow_date.isoformat() if self.borrow_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'status': self.status,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'user_name': self.user.full_name if self.user else None,
            'book_title': self.book.title if self.book else None
        }



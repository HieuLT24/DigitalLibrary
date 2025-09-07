

from . import db

class BorrowRequest(db.Model):
    __tablename__ = "borrow_request"

    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50))          # pending / approved / rejected / converted
    reject_reason = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id"), nullable=False)

    book = db.relationship("Book", backref="borrow_requests")
    user = db.relationship("User", back_populates="borrow_requests")



from . import db

class BorrowRequest(db.Model):
    __tablename__ = "borrow_request"
    
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50))
    reject_reason = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    
    def to_dict(self):
        return {
            'request_id': self.request_id,
            'request_date': self.request_date.isoformat() if self.request_date else None,
            'status': self.status,
            'reject_reason': self.reject_reason,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else None
        }


from . import db
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
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'full_name': self.full_name,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'status': self.status
        }


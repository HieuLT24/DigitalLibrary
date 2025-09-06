

from . import db

class Notification(db.Model):
    __tablename__ = "notification"
    
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    sent_date = db.Column(db.Date)
    type = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)


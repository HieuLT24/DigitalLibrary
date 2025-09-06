

from . import db

class Notification(db.Model):
    __tablename__ = "notification"
    
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    sent_date = db.Column(db.Date)
    type = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    
    def to_dict(self):
        return {
            'notification_id': self.notification_id,
            'content': self.content,
            'sent_date': self.sent_date.isoformat() if self.sent_date else None,
            'type': self.type,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else None
        }


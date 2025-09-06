
from . import db

class Category(db.Model):
    __tablename__ = "category"
    
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    books = db.relationship("Book", backref="category", lazy=True)
    
    def to_dict(self):
        return {
            'category_id': self.category_id,
            'name': self.name,
        }


from . import db

class Author(db.Model):
    __tablename__ = "author"
    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    
    books = db.relationship("Book", backref="author", lazy=True)

    def to_dict(self):
        return {
            "author_id": self.author_id,
            "name": self.name
        }
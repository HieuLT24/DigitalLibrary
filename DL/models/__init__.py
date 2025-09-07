from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .book import Book
from .author import Author
from .category import Category
from .borrow_slip import BorrowSlip
from .borrow_request import BorrowRequest
from .notification import Notification

#export
__all__ = [
    'db',
    'User',
    'Book', 
    'Author',
    'Category',
    'BorrowSlip',
    'BorrowRequest',
    'Notification'
]

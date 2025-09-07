from DL.models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import re

class UserService:
    def get_user_by_id(self, user_id):
        return User.query.get(user_id)
    
    def get_user_by_username(self, username):
        return User.query.filter(db.func.lower(User.username) == db.func.lower(username)).first()
    
    def get_user_by_email(self, email):
        return User.query.filter(db.func.lower(User.email) == db.func.lower(email)).first()
    
    def create_user(self, username, email, password):
        if self.get_user_by_username(username):
            raise ValueError("USERNAME_EXISTS")
        if self.get_user_by_email(email):
            raise ValueError("EMAIL_EXISTS")

        hashed = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed, full_name=username, role='user')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            if self.get_user_by_username(username):
                raise ValueError("USERNAME_EXISTS")
            if self.get_user_by_email(email):
                raise ValueError("EMAIL_EXISTS")
            raise
        return user

    def update_user_profile(self, user_id, full_name=None, email=None, phone_number=None, gender=None):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("USER_NOT_FOUND")
        if email and email.lower() != (user.email or '').lower():
            if self.get_user_by_email(email):
                raise ValueError("EMAIL_EXISTS")
            user.email = email
        if full_name is not None:
            user.full_name = full_name
        if phone_number is not None:
            digits = ''.join(ch for ch in phone_number if ch.isdigit())
            if not re.fullmatch(r"0\d{9,10}", digits):
                raise ValueError("INVALID_PHONE_LENGTH")
            user.phone_number = digits
        if gender is not None:
            user.gender = gender
        db.session.commit()
        return user

    def update_user_password(self, user_id, current_password, new_password):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("USER_NOT_FOUND")
        if not check_password_hash(user.password, current_password):
            raise ValueError("INVALID_PASSWORD")
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return True
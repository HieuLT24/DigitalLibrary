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

    def create_user(self, username, email, password, full_name=None, phone_number=None, gender=None):
        # Kiểm tra trùng
        if self.get_user_by_username(username):
            raise ValueError("USERNAME_EXISTS")
        if self.get_user_by_email(email):
            raise ValueError("EMAIL_EXISTS")

        # Chuẩn hóa & validate dữ liệu bổ sung
        final_full_name = (full_name or username or "").strip()
        if len(final_full_name) < 2:
            raise ValueError("FULLNAME_TOO_SHORT")

        digits_phone = None
        if phone_number:
            digits_phone = ''.join(ch for ch in phone_number if ch.isdigit())
            # 0 + 9 hoặc 10 chữ số phía sau (tổng 10 hoặc 11)
            if not re.fullmatch(r"0\d{9,10}", digits_phone):
                raise ValueError("INVALID_PHONE")

        allowed_genders = {"Nam", "Nữ", "Khác", None, ""}
        if gender not in allowed_genders:
            raise ValueError("INVALID_GENDER")

        hashed = generate_password_hash(password)
        user = User(
            username=username,
            email=email,
            password=hashed,
            full_name=final_full_name,
            role='user',
            status='active',
            phone_number=digits_phone,
            gender=gender if gender in {"Nam", "Nữ", "Khác"} else None,
            is_active=1
        )
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
            if len(full_name.strip()) < 2:
                raise ValueError("FULLNAME_TOO_SHORT")
            user.full_name = full_name.strip()
        if phone_number is not None:
            digits = ''.join(ch for ch in phone_number if ch.isdigit())
            if not re.fullmatch(r"0\d{9,10}", digits):
                raise ValueError("INVALID_PHONE_LENGTH")
            user.phone_number = digits
        if gender is not None:
            if gender not in {"Nam", "Nữ", "Khác"}:
                raise ValueError("INVALID_GENDER")
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
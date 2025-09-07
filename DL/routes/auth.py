from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from DL.services.user_service import UserService
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = UserService().get_user_by_username(username)
        if not user or not check_password_hash(user.password, password):
            return "Tên đăng nhập hoặc mật khẩu không chính xác!"
        login_user(user)
        return redirect("/")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Mật khẩu không khớp!"
        service = UserService()
        try:
            user = service.create_user(username, email, password)
        except ValueError as e:
            msg = str(e)
            if msg == "USERNAME_EXISTS":
                return "Tên đăng nhập đã tồn tại!"
            if msg == "EMAIL_EXISTS":
                return "Email đã tồn tại!"
            return "Đăng ký thất bại!"
        except IntegrityError:
            return "Đăng ký thất bại do trùng lặp!"
        login_user(user)
        return redirect(url_for('auth.login'))
    return render_template("register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
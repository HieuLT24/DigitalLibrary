from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError
from urllib.parse import urlparse, urljoin

from DL.services.user_service import UserService

auth_bp = Blueprint('auth', __name__)

def is_safe_url(target):
    if not target:
        return False
    host_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (test_url.scheme in ('http','https') and
            host_url.netloc == test_url.netloc)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    next_url = request.args.get('next')
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")
        service = UserService()
        user = service.get_user_by_username(username)
        if not user or not check_password_hash(user.password, password):
            flash("Tên đăng nhập hoặc mật khẩu không chính xác!", "danger")
            return redirect(url_for('auth.login', next=next_url) if next_url else url_for('auth.login'))
        login_user(user)
        flash("Đăng nhập thành công", "success")
        if next_url and is_safe_url(next_url):
            return redirect(next_url)
        return redirect(url_for('main.index'))
    return render_template("login.html", next_url=next_url)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == "POST":
        form = request.form
        username = form.get("username","").strip()
        email = form.get("email","").strip()
        password = form.get("password","")
        confirm_password = form.get("confirm_password","")
        full_name = form.get("full_name","").strip()
        phone_number = form.get("phone_number","").strip()
        gender = form.get("gender")  # Nam / Nữ / Khác

        # Kiểm tra cơ bản
        if password != confirm_password:
            flash("Mật khẩu xác nhận không khớp!", "danger")
            return render_template("register.html", form=form)
        if len(password) < 6:
            flash("Mật khẩu tối thiểu 6 ký tự", "warning")
            return render_template("register.html", form=form)
        if len(full_name) < 2:
            flash("Họ tên tối thiểu 2 ký tự", "warning")
            return render_template("register.html", form=form)
        if phone_number:
            digits = ''.join(ch for ch in phone_number if ch.isdigit())
            # 0 + 9 hoặc 10 chữ số
            import re
            if not re.fullmatch(r"0\d{9,10}", digits):
                flash("Số điện thoại không hợp lệ (phải bắt đầu 0 và dài 10-11 số)", "danger")
                return render_template("register.html", form=form)
        if gender not in ("Nam","Nữ","Khác", None, ""):
            flash("Giới tính không hợp lệ", "danger")
            return render_template("register.html", form=form)

        service = UserService()
        try:
            user = service.create_user(
                username=username,
                email=email,
                password=password,
                full_name=full_name,
                phone_number=phone_number,
                gender=gender
            )
        except ValueError as e:
            code = str(e)
            msg_map = {
                "USERNAME_EXISTS": "Tên đăng nhập đã tồn tại!",
                "EMAIL_EXISTS": "Email đã tồn tại!",
                "FULLNAME_TOO_SHORT": "Họ tên tối thiểu 2 ký tự!",
                "INVALID_PHONE": "Số điện thoại không hợp lệ!",
                "INVALID_GENDER": "Giới tính không hợp lệ!"
            }
            flash(msg_map.get(code, "Đăng ký thất bại!"), "danger")
            return render_template("register.html", form=form)
        except IntegrityError:
            flash("Đăng ký thất bại do trùng dữ liệu!", "danger")
            return render_template("register.html", form=form)
        flash("Đăng ký thành công, vui lòng đăng nhập", "success")
        return redirect(url_for('auth.login'))
    # GET
    return render_template("register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Đã đăng xuất", "success")
    return redirect(url_for('main.index'))
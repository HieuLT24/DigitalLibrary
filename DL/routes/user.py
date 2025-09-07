from flask import Blueprint, render_template, redirect, url_for, request, flash

from DL.models import BorrowSlip, Book
from DL.services.borrow_service import BorrowService
from DL.services.user_service import UserService
from flask_login import current_user, login_required

user_bp = Blueprint('user', __name__)

@user_bp.route("/profile")
@login_required
def user_profile():
    service = UserService()
    user = service.get_user_by_id(current_user.user_id)
    if not user:
        return redirect(url_for('auth.login'))
    user_data = {
        "username": user.username,
        "name": user.full_name,
        "borrow_count": len(user.borrow_slips) if hasattr(user, 'borrow_slips') else 0,
        "pending_books": len(user.borrow_requests) if hasattr(user, 'borrow_requests') else 0,
        "email": user.email,
        "phone_number": user.phone_number,
        "gender": user.gender
    }
    return render_template("user_profile.html", user=user_data)


@user_bp.route("/profile/update", methods=["POST"])
@login_required
def update_profile():
    service = UserService()
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    gender = request.form.get('gender')
    try:
        service.update_user_profile(current_user.user_id, full_name=full_name, email=email, phone_number=phone_number, gender=gender)
        flash('Cập nhật thông tin thành công', 'success')
    except ValueError as e:
        msg = str(e)
        if msg == 'EMAIL_EXISTS':
            flash('Email đã tồn tại', 'danger')
        elif msg == 'INVALID_PHONE_LENGTH':
            flash('Số điện thoại tối đa 11 chữ số', 'danger')
        elif msg == 'USER_NOT_FOUND':
            flash('Không tìm thấy người dùng', 'danger')
        else:
            flash('Cập nhật thất bại', 'danger')
    return redirect(url_for('user.user_profile'))


@user_bp.route("/profile/password", methods=["POST"])
@login_required
def update_password():
    service = UserService()
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    if not new_password or new_password != confirm_password:
        flash('Xác nhận mật khẩu không khớp', 'danger')
        return redirect(url_for('user.user_profile'))
    try:
        service.update_user_password(current_user.user_id, current_password, new_password)
        flash('Đổi mật khẩu thành công', 'success')
    except ValueError as e:
        if str(e) == 'INVALID_PASSWORD':
            flash('Mật khẩu cũ không đúng', 'danger')
        elif str(e) == 'USER_NOT_FOUND':
            flash('Không tìm thấy người dùng', 'danger')
        else:
            flash('Đổi mật khẩu thất bại', 'danger')
    return redirect(url_for('user.user_profile'))

@user_bp.route("/borrowed")
@login_required
def borrowed_list():
    slips = BorrowSlip.query.filter_by(user_id=current_user.user_id, status='borrowed') \
                            .join(Book, BorrowSlip.book_id == Book.book_id).all()
    return render_template("borrowed_list.html", slips=slips)

@user_bp.route("/requests")
@login_required
def request_list():
    borrow_service = BorrowService()
    # Lấy cả pending & approved để user thấy
    requests = borrow_service.get_user_requests(current_user.user_id, statuses=["pending","approved"])
    return render_template("request_list.html", requests=requests)

@user_bp.route("/loans")
@login_required
def loans_overview():
    borrow_service = BorrowService()
    data = borrow_service.get_user_overview(current_user.user_id)
    return render_template("my_loans.html",
                           borrowed=data["borrowed"],
                           pending=data["pending"],
                           approved=data["approved"])

@user_bp.route("/requests/<int:request_id>/cancel", methods=["POST"])
@login_required
def cancel_request(request_id):
    service = BorrowService()
    try:
        service.cancel_request(current_user.user_id, request_id)
        flash("Đã hủy yêu cầu mượn.", "success")
    except ValueError as e:
        code = str(e)
        msg = {
            "REQUEST_NOT_FOUND": "Không tìm thấy yêu cầu.",
            "CANNOT_CANCEL": "Yêu cầu này không thể hủy."
        }.get(code, "Hủy yêu cầu thất bại.")
        flash(msg, "danger")
    return redirect(url_for('user.loans_overview'))
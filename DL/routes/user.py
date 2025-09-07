from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required

from DL.models import BorrowSlip, Book, BorrowRequest
from DL.services.borrow_service import BorrowService
from DL.services.user_service import UserService

user_bp = Blueprint('user', __name__)


@user_bp.route("/profile")
@login_required
def user_profile():
    """
    Trang hồ sơ người dùng.
    pending_books = số yêu cầu đang ACTIVE (pending + approved) để user thấy còn bao nhiêu yêu cầu chờ xử lý/giao.
    """
    service = UserService()
    user = service.get_user_by_id(current_user.user_id)
    if not user:
        return redirect(url_for('auth.login'))

    # Đếm borrowed slips (status=borrowed)
    borrow_count = 0
    if hasattr(user, 'borrow_slips'):
        borrow_count = sum(1 for s in user.borrow_slips if getattr(s, 'status', None) == 'borrowed')

    # Đếm active requests (pending + approved)
    active_requests = 0
    if hasattr(user, 'borrow_requests'):
        active_requests = sum(1 for r in user.borrow_requests if r.status in ('pending', 'approved'))

    user_data = {
        "username": user.username,
        "name": user.full_name,
        "borrow_count": borrow_count,
        "pending_books": active_requests,
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
        service.update_user_profile(
            current_user.user_id,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            gender=gender
        )
        flash('Cập nhật thông tin thành công', 'success')
    except ValueError as e:
        msg = str(e)
        mapping = {
            'EMAIL_EXISTS': 'Email đã tồn tại',
            'INVALID_PHONE_LENGTH': 'Số điện thoại tối đa 11 chữ số',
            'USER_NOT_FOUND': 'Không tìm thấy người dùng'
        }
        flash(mapping.get(msg, 'Cập nhật thất bại'), 'danger')
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
        mapping = {
            'INVALID_PASSWORD': 'Mật khẩu cũ không đúng',
            'USER_NOT_FOUND': 'Không tìm thấy người dùng'
        }
        flash(mapping.get(str(e), 'Đổi mật khẩu thất bại'), 'danger')
    return redirect(url_for('user.user_profile'))


@user_bp.route("/borrowed")
@login_required
def borrowed_list():
    """
    Danh sách phiếu đang mượn thực tế.
    """
    slips = (BorrowSlip.query
             .filter_by(user_id=current_user.user_id, status='borrowed')
             .join(Book, BorrowSlip.book_id == Book.book_id)
             .all())
    return render_template("borrowed_list.html", slips=slips)


@user_bp.route("/requests")
@login_required
def request_list():
    """
    Danh sách yêu cầu đang hoạt động (pending + approved) – TÁCH RIÊNG
    Nếu muốn thêm cả canceled/rejected, sửa statuses=... hoặc bỏ tham số để lấy tất.
    """
    borrow_service = BorrowService()
    requests_q = borrow_service.get_user_requests(
        current_user.user_id,
        statuses=["pending", "approved"]
    )
    return render_template("request_list.html", requests=requests_q)


@user_bp.route("/loans")
@login_required
def loans_overview():
    """
    Trang tổng hợp: đang mượn, chờ duyệt, đã duyệt, + (gộp failed ở template = canceled + rejected).
    Service đã trả canceled & rejected, ta truyền đầy đủ để template gộp.
    """
    borrow_service = BorrowService()
    data = borrow_service.get_user_overview(current_user.user_id)
    return render_template(
        "my_loans.html",
        borrowed=data["borrowed"],
        pending=data["pending"],
        approved=data["approved"],
        canceled=data["canceled"],
        rejected=data["rejected"]
    )


@user_bp.route("/requests/<int:request_id>/cancel", methods=["POST"])
@login_required
def cancel_request(request_id):
    """
    Hủy yêu cầu.
    MẶC ĐỊNH: chỉ hủy được khi pending.
    Nếu muốn hủy cả approved trước khi nhận sách:
      - Mở rộng BorrowService.cancel_request cho phép status in ('pending','approved')
      - Cập nhật template approved thêm nút hủy.
    """
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

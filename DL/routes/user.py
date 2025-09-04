from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__)

@user_bp.route("/profile")
def user_profile():
    user_data = {
        "name": "Nguyen Van A",
        "borrow_count": 36,
        "pending_books": 2,
        "email": "vana@example.com",
        "phone": "0123456789",
        "gender": "Nam"
    }
    return render_template("user_profile.html", user=user_data)

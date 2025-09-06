from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/requests")
def admin_requests():
    # dữ liệu mẫu
    requests = [
        {"book": "The Great Gatsby", "user": "John Smith", "req_date": "Jun 12, 2023", "due_date": "Jul 12, 2023", "status": "Pending"},
        {"book": "To Kill a Mockingbird", "user": "Sarah Johnson", "req_date": "Jun 10, 2023", "due_date": "Jul 10, 2023", "status": "Approved"},
        {"book": "1984", "user": "Michael Brown", "req_date": "Jun 8, 2023", "due_date": "Jun 22, 2023", "status": "Rejected"},
        {"book": "Pride and Prejudice", "user": "Emily Davis", "req_date": "Jun 5, 2023", "due_date": "Jun 19, 2023", "status": "Overdue"}
    ]
    return render_template("admin_templates/admin_requests.html", requests=requests)

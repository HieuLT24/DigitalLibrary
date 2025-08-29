from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/book/<int:book_id>")
def book_detail(book_id):
    sample_book = {
        "id": book_id,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "978-0-7432-7356-5",
        "genre": "Tiểu thuyết",
        "description": "Một trong những tác phẩm kinh điển nhất của văn học Mỹ..."
    }
    return render_template("book_detail.html", book=sample_book)


@app.route("/profile")
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

@app.route("/admin/requests")
def admin_requests():
    # dữ liệu mẫu
    requests = [
        {"book": "The Great Gatsby", "user": "John Smith", "req_date": "Jun 12, 2023", "due_date": "Jul 12, 2023", "status": "Pending"},
        {"book": "To Kill a Mockingbird", "user": "Sarah Johnson", "req_date": "Jun 10, 2023", "due_date": "Jul 10, 2023", "status": "Approved"},
        {"book": "1984", "user": "Michael Brown", "req_date": "Jun 8, 2023", "due_date": "Jun 22, 2023", "status": "Rejected"},
        {"book": "Pride and Prejudice", "user": "Emily Davis", "req_date": "Jun 5, 2023", "due_date": "Jun 19, 2023", "status": "Overdue"}
    ]
    return render_template("admin_templates/admin_requests.html", requests=requests)







if __name__ =="__main__":
    with app.app_context():
        app.run(debug=True)
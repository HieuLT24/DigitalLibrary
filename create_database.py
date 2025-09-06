
from DL import create_app, db
from DL.models import User, Book, Author, Category, BorrowSlip, BorrowRequest, Notification

def create_database_tables():
    app = create_app()
    
    with app.app_context():
        try:
            db.create_all()

            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            for table in tables:
                print(f"   ✓ {table}")
            
            
        except Exception as e:
            print(f"❌ Lỗi khi tạo bảng: {e}")
if __name__ == "__main__":
    create_database_tables()

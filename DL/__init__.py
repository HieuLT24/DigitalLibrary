from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
import cloudinary

from DL.models import db, User

migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    app.config.from_object('DL.config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_time_helpers():
        from datetime import datetime, date
        return {
            'now': datetime.utcnow,
            'today': date.today()
        }

    from DL import models
    
    from DL.routes.main import main_bp
    from DL.routes.admin import admin_bp
    from DL.routes.user import user_bp
    from DL.routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRET"]
    )
    
    return app
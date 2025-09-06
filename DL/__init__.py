from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Khởi tạo extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load config
    if config_name == 'development':
        app.config.from_object('DL.config.DevelopmentConfig')
    elif config_name == 'production':
        app.config.from_object('DL.config.ProductionConfig')
    else:
        app.config.from_object('DL.config.Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from DL.routes.main import main_bp
    from DL.routes.admin import admin_bp
    from DL.routes.user import user_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')
    
    return app
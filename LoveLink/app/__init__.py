from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate   # ✅ ADD THIS

db = SQLAlchemy()
migrate = Migrate()   # ✅ ADD THIS

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # ✅ ADD THESE 3 LINES (ADMIN SETTINGS)
    app.config['ADMIN_USERNAME'] = 'admin'
    app.config['ADMIN_PASSWORD'] = '1234'
    app.config['SECRET_KEY'] = 'supersecretkey'

    db.init_app(app)
    migrate.init_app(app, db)   # ✅ ADD THIS

    from .routes import main
    app.register_blueprint(main)

    # 👇 REGISTER ADMIN
    from .admin_routes import admin
    app.register_blueprint(admin)

    return app

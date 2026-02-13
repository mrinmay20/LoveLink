import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///lovelink.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "app/static/uploads"
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "1234"

    #UPLOAD_FOLDER = os.path.join("app", "static", "uploads")


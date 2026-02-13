import uuid
from datetime import datetime
from . import db

class LovePage(db.Model):

    id = db.Column(db.String(8), primary_key=True, default=lambda: uuid.uuid4().hex[:8])

    your_name = db.Column(db.String(100), nullable=False)
    partner_name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    your_photo = db.Column(db.String(200))
    partner_photo = db.Column(db.String(200))

    theme = db.Column(db.String(50))
    music = db.Column(db.String(50))
    plan = db.Column(db.String(20))
    payment_status = db.Column(db.String(20), default="pending")
    custom_music = db.Column(db.String(200))
    video_file = db.Column(db.String(200))
    password = db.Column(db.String(100))

    views = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    expiry_date = db.Column(db.DateTime)

    


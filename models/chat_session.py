# models/chat_session.py

from database.db import db

class ChatSession(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    mobile = db.Column(
        db.String(20),
        unique=True
    )

    step = db.Column(
        db.String(100)
    )

    temp_data = db.Column(
        db.Text
    )

    updated_at = db.Column(
        db.DateTime
    )
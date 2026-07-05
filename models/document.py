# models/document.py

from database.db import db
from datetime import datetime


class ComplaintDocument(db.Model):

    __tablename__ = "complaint_documents"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    complaint_id = db.Column(
        db.Integer,
        db.ForeignKey('complaints.id')
    )

    file_name = db.Column(
        db.String(255)
    )

    file_path = db.Column(
        db.String(500)
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
from database.db import db

class Service(db.Model):

    __tablename__ = "service"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey('department.id'),
        nullable=False
    )

    service_name = db.Column(
        db.Text,
        nullable=False
    )

    time_limit = db.Column(
        db.Integer
    )

    designated_officer = db.Column(
        db.Text
    )

    appellate_authority = db.Column(
        db.Text
    )

    notification = db.Column(
        db.Text
    )
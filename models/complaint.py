from database.db import db
from datetime import datetime


class Complaint(db.Model):

    __tablename__ = "complaints"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    complaint_no = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    applicant_name = db.Column(
        db.String(200),
        nullable=False
    )

    mobile = db.Column(
        db.String(20),
        nullable=False
    )

    email = db.Column(
        db.String(100)
    )

    address = db.Column(
        db.Text,
        nullable=False
    )

    office_name = db.Column(
        db.String(200),
        nullable=False
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("department.id"),
        nullable=False
    )

    service_id = db.Column(
        db.Integer,
        db.ForeignKey("service.id"),
        nullable=False
    )

    application_number = db.Column(
        db.String(100),
        nullable=False
    )

    application_date = db.Column(
        db.Date,
        nullable=False
    )

    grievance = db.Column(
        db.Text,
        nullable=False
    )

    relief_sought = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(100),
        default="Received"
    )

    remarks = db.Column(
        db.Text
    )

    # NEW FIELD
    source = db.Column(
        db.String(20),
        default="Website"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationships

    department = db.relationship(
        "Department"
    )

    service = db.relationship(
        "Service"
    )

    documents = db.relationship(
        "ComplaintDocument",
        backref="complaint",
        cascade="all, delete-orphan"
    )

    def __repr__(self):

        return (
            f"<Complaint {self.complaint_no}>"
        )
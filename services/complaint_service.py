from datetime import datetime

from models.complaint import Complaint
from database.db import db


def generate_complaint_number():
    """
    Generates complaint number like:
    PBTRAC-2026-000001
    """

    total = Complaint.query.count() + 1

    year = datetime.now().year

    return f"PBTRAC-{year}-{total:06d}"


def create_complaint(
    applicant_name,
    mobile,
    email,
    address,
    office_name,
    department_id,
    service_id,
    application_number,
    application_date,
    grievance,
    relief_sought,
    source="Website"
):
    """
    Creates a complaint and saves it to database.
    """

    complaint = Complaint(

        complaint_no=generate_complaint_number(),

        applicant_name=applicant_name,

        mobile=mobile,

        email=email,

        address=address,

        office_name=office_name,

        department_id=department_id,

        service_id=service_id,

        application_number=application_number,

        application_date=application_date,

        grievance=grievance,

        relief_sought=relief_sought,

        status="Received",

        source=source
    )

    db.session.add(complaint)

    db.session.commit()

    return complaint
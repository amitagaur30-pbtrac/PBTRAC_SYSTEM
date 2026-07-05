import os
from datetime import datetime, date

from werkzeug.utils import secure_filename

from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify

from database.db import db

from models.complaint import Complaint
from models.department import Department
from models.service import Service
from models.document import ComplaintDocument

from services.complaint_service import create_complaint


citizen_bp = Blueprint(
    "citizen",
    __name__
)


ALLOWED_EXTENSIONS = {
    "pdf",
    "jpg",
    "jpeg",
    "png"
}


def allowed_file(filename):

    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# --------------------------------------------------
# Get services for selected department
# --------------------------------------------------

@citizen_bp.route("/get_services/<int:department_id>")
def get_services(department_id):

    services = Service.query.filter_by(
        department_id=department_id
    ).all()

    data = []

    for service in services:

        data.append({
            "id": service.id,
            "name": service.service_name
        })

    return jsonify(data)


# --------------------------------------------------
# Show departments (testing)
# --------------------------------------------------

@citizen_bp.route("/departments")
def departments():

    departments = Department.query.all()

    output = ""

    for dept in departments:

        output += (
            f"{dept.id} - "
            f"{dept.code} - "
            f"{dept.name}<br>"
        )

    return output


# --------------------------------------------------
# Show services (testing)
# --------------------------------------------------

@citizen_bp.route("/services")
def services():

    services = Service.query.limit(20).all()

    output = ""

    for service in services:

        output += f"""
        ID: {service.id}<br>
        Service: {service.service_name}<br>
        <hr>
        """

    if output == "":
        output = "No services found"

    return output


# --------------------------------------------------
# Complaint Registration
# --------------------------------------------------

@citizen_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        application_date = datetime.strptime(
            request.form["application_date"],
            "%Y-%m-%d"
        ).date()

        complaint = create_complaint(

            applicant_name=request.form["name"],

            mobile=request.form["mobile"],

            email=request.form.get("email"),

            address=request.form["address"],

            office_name=request.form["office_name"],

            department_id=int(
                request.form["department_id"]
            ),

            service_id=int(
                request.form["service_id"]
            ),

            application_number=request.form[
                "application_number"
            ],

            application_date=application_date,

            grievance=request.form[
                "description"
            ],

            relief_sought=request.form[
                "relief_sought"
            ]

        )

        # ---------------------------------------
        # Save uploaded documents
        # ---------------------------------------

        files = request.files.getlist(
            "documents"
        )

        os.makedirs(
            "uploads",
            exist_ok=True
        )

        for file in files:

            if (
                file.filename != ""
                and
                allowed_file(file.filename)
            ):

                filename = secure_filename(
                    file.filename
                )

                filepath = os.path.join(
                    "uploads",
                    filename
                )

                file.save(filepath)

                document = ComplaintDocument(

                    complaint_id=complaint.id,

                    file_name=filename,

                    file_path=filepath

                )

                db.session.add(document)

        db.session.commit()

        return f"""
        <h2>
        Complaint Registered Successfully
        </h2>

        <br>

        <h3>
        Complaint Number:
        {complaint.complaint_no}
        </h3>

        <br>

        <a href='/'>
        Go to Home
        </a>
        """

    departments = db.session.query(
        Department
    ).join(
        Service,
        Department.id == Service.department_id
    ).distinct().all()

    return render_template(
        "register.html",
        departments=departments,
        today=date.today().isoformat()
    )


# --------------------------------------------------
# Track Complaint
# --------------------------------------------------

@citizen_bp.route(
    "/track",
    methods=["GET", "POST"]
)
def track():

    complaint = None

    if request.method == "POST":

        complaint_no = request.form[
            "complaint_no"
        ]

        complaint = Complaint.query.filter_by(
            complaint_no=complaint_no
        ).first()

    return render_template(
        "track.html",
        complaint=complaint
    )
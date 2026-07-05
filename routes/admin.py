import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    session,
    send_from_directory
)

from database.db import db
from models.admin import Admin
from models.complaint import Complaint


admin_bp = Blueprint(
    "admin",
    __name__
)


# ==========================
# ADMIN LOGIN
# ==========================

@admin_bp.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def login():

    error = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(
            username=username,
            password=password
        ).first()

        if admin:

            session["admin"] = username

            flash(
                "Login successful",
                "success"
            )

            return redirect("/admin")

        else:

            error = (
                "Invalid username or password"
            )

    return render_template(
        "admin_login.html",
        error=error
    )


# ==========================
# ADMIN DASHBOARD
# ==========================

@admin_bp.route("/admin")
def dashboard():

    if "admin" not in session:
        return redirect("/admin/login")

    complaints = Complaint.query.order_by(
        Complaint.id.desc()
    ).all()

    return render_template(
        "admin_dashboard.html",
        complaints=complaints
    )


# ==========================
# VIEW COMPLAINT DETAILS
# ==========================

@admin_bp.route(
    "/admin/complaint/<int:id>"
)
def complaint_detail(id):

    if "admin" not in session:
        return redirect("/admin/login")

    complaint = db.session.get(
        Complaint,
        id
    )

    if not complaint:

        flash(
            "Complaint not found",
            "danger"
        )

        return redirect("/admin")

    return render_template(
        "complaint_detail.html",
        complaint=complaint
    )


# ==========================
# UPDATE STATUS + REMARKS
# ==========================

@admin_bp.route(
    "/update_status/<int:id>",
    methods=["POST"]
)
def update_status(id):

    if "admin" not in session:
        return redirect("/admin/login")

    complaint = db.session.get(
        Complaint,
        id
    )

    if not complaint:

        flash(
            "Complaint not found",
            "danger"
        )

        return redirect("/admin")

    complaint.status = request.form.get(
        "status"
    )

    complaint.remarks = request.form.get(
        "remarks"
    )

    db.session.commit()

    flash(
        "Complaint updated successfully",
        "success"
    )

    return redirect(
        f"/admin/complaint/{id}"
    )


# ==========================
# SERVE UPLOADED DOCUMENTS
# ==========================

@admin_bp.route(
    "/uploads/<filename>"
)
def uploaded_file(filename):

    upload_folder = os.path.join(
        os.getcwd(),
        "uploads"
    )

    return send_from_directory(
        upload_folder,
        filename
    )


# ==========================
# LOGOUT
# ==========================

@admin_bp.route("/admin/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully",
        "success"
    )

    return redirect(
        "/admin/login"
    )
from database.db import db
from models.admin import Admin


def create_admin():

    existing = Admin.query.filter_by(
        username="admin"
    ).first()

    if existing:

        print("Admin already exists.")
        return

    admin = Admin(
        username="admin",
        password="admin123"
    )

    db.session.add(admin)
    db.session.commit()

    print("Admin created successfully.")
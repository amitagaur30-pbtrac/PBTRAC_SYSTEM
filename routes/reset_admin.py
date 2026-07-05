from app import app
from database.db import db
from models.admin import Admin

with app.app_context():

    admin = Admin.query.first()

    if admin:

        admin.username = "admin"
        admin.password = "admin123"

        db.session.commit()

        print("Admin password reset successfully")

    else:

        print("No admin found")
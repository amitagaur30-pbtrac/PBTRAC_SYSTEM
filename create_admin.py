from app import app
from database.db import db

from models.admin import Admin

with app.app_context():

    admin = Admin(
        username="admin",
        password="admin123"
    )

    db.session.add(admin)
    db.session.commit()

    print("Admin created")
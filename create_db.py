from models.admin import Admin
from app import app
from database.db import db

from models.complaint import Complaint
from models.admin import Admin
from models.department import Department
from models.service import Service
from models.document import ComplaintDocument

with app.app_context():

    db.create_all()

    print("Database created successfully")
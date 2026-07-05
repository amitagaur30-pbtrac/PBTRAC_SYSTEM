from app import app
from database.db import db
from models.service import Service

with app.app_context():

    deleted = Service.query.delete()

    db.session.commit()

    print(f"{deleted} services deleted.")
from create_admin import create_admin
from seed_departments import seed_departments
from import_services import import_services

from models.department import Department
from models.service import Service


def initialize_database():

    create_admin()

    if Department.query.count() == 0:
        seed_departments()

    if Service.query.count() == 0:
        import_services()

    print("Database initialized")
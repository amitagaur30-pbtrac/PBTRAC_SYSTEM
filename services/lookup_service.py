from models.department import Department
from models.service import Service


def get_departments():

    departments = (
        Department.query
        .order_by(Department.name)
        .all()
    )

    return departments


def get_department(department_id):

    return Department.query.get(
        department_id
    )


def get_services(department_id):

    services = (
        Service.query
        .filter_by(
            department_id=department_id
        )
        .order_by(
            Service.service_name
        )
        .all()
    )

    return services


def get_service(service_id):

    return Service.query.get(
        service_id
    )
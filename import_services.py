from app import app
from database.db import db

from models.department import Department
from models.service import Service

import pandas as pd

# Read Excel file
df = pd.read_excel("services.xlsx")

with app.app_context():

    imported = 0

    # Mapping between Excel department names
    # and Department table names

    mapping = {

        # Direct departments

        "Agriculture":
            "Department of Agriculture",

        "Animal Husbandry":
            "Department of Animal Husbandry, Dairy Development and Fisheries",

        "Dairy Development":
            "Department of Animal Husbandry, Dairy Development and Fisheries",

        "Excise and Taxation":
            "Department of Excise and Taxation",

        "Food, Civil Supplies and Consumer Affairs":
            "Department of Food, Civil Supplies and Consumer Affairs",

        "Forest and Wildlife Preservation":
            "Department of Forest and Wild Life Preservation",

        "Health and Family Welfare":
            "Department of Health & Family Welfare",

        "Higher Education and Language":
            "Department of Higher Education and Languages",

        "Home and Justice":
            "Department of Home Affairs and Justice",

        "Industries and Commerce":
            "Department of Industries and Commerce",

        "Labour Dept.":
            "Department of Labour",

        "Local Government":
            "Department of Local Government",

        "Medical Education and Research":
            "Department of Medical Education and Research",

        "Mines and Geology":
            "Department of Mines and Geology",

        "Department of Personnel":
            "Department of Personnel",

        "Revenue":
            "Department of Revenue, Rehabilitation & Disaster Management",

        "Rural Development":
            "Department of Rural Development and Panchayat",

        "School Education":
            "Department of School Education",

        "Transport Department":
            "Department of Transport",

        "Water Resources":
            "Department of Water Resources",

        "Welfare of Freedom Fighters":
            "Department of Welfare of Freedom Fighters",

        # Special cases

        "Investment Promotion":
            "Department of Investment Promotion",

        "Governance Reforms and Public Grievances":
            "Department of Good Governance and Information Technology",

        "Power/ Electricity":
            "Department of Power",

        "Department of Housing and Urban Development (PUDA)":
            "Department of Housing and Urban Development Authority",

        "Town and Country Planning":
            "Department of Housing and Urban Development Authority",

        "Social Justice & Empowerment & Minorities":
            "Department of Social Justice, Empowerment and Minorities",

        "Social Security & Development of Women & Child":
            "Department of Social Security and Women & Child Development",

        "Science, Technology & Environment (PPCB)":
            "Department of Science, Technology & Environment",

        "Department of Tourism, Culture Affairs, Archaeology, Museum and Archives":
            "Department of Tourism and Cultural Affairs",

        "Technical Education & Industrial Training":
            "Department of Technical Education and Industrial Training",

        # Institutions

        "Agro Industries Corporation Ltd.":
            "Department of Industries and Commerce",

        "Punjab Small Industries & Export Corporation Ltd.":
            "Department of Industries and Commerce",

        "Punjab State Co-operative Fedration (Puncofed)":
            "Department of Cooperation",

        "Punjab Agriculture University":
            "Department of Agriculture",

        "Punjab State Veterinary Council":
            "Department of Animal Husbandry, Dairy Development and Fisheries",

        "Food & Drug Administration":
            "Department of Health & Family Welfare",

        "Public Works Department (Roads & Bridges)":
            "Department of Public Works",

        "Rural Water Supply and Sanitation":
            "Department of Water Supply and Sanitation"
    }

    for _, row in df.iterrows():

        dept_name = str(
            row["Department"]
        ).strip()

        service_name = str(
            row["Name of Service"]
        ).strip()

        # Skip empty rows

        if (
            service_name == ""
            or service_name.lower() == "nan"
            or service_name.lower() == "name of service"
        ):
            continue

        # Universities / Institutions under TEIT

        if (
            "Technical University" in dept_name
            or "State University" in dept_name
            or "Punjab State Board of Technical Education" in dept_name
        ):

            dept_name = (
                "Department of Technical Education and Industrial Training"
            )

        # Apply mapping

        elif dept_name in mapping:

            dept_name = mapping[dept_name]

        # Find Department

        department = Department.query.filter_by(
            name=dept_name
        ).first()

        if department:

            service = Service(

                department_id=department.id,

                service_name=service_name
            )

            db.session.add(service)

            imported += 1

        else:

            print(
                "Department not found:",
                dept_name
            )

    db.session.commit()

    print("Imported:", imported)
from app import app
from database.db import db
from models.department import Department

departments = [

    ("AGRI/001", "Department of Agriculture"),
    ("AHDD/002", "Department of Animal Husbandry, Dairy Development and Fisheries"),
    ("CIVA/003", "Department of Civil Aviation"),
    ("COOP/004", "Department of Cooperation"),
    ("DSWE/005", "Department of Defence Services Welfare"),
    ("ELEC/006", "Department of Elections"),
    ("EGSDT/007", "Department of Employment Generation, Skill Development and Training"),
    ("EXTN/008", "Department of Excise and Taxation"),
    ("FINE/009", "Department of Finance"),
    ("DCSCA/010", "Department of Food, Civil Supplies and Consumer Affairs"),
    ("FWLP/011", "Department of Forest and Wild Life Preservation"),
    ("GEAN/012", "Department of General Administration"),
    ("GDIT/013", "Department of Good Governance and Information Technology"),
    ("HFWE/014", "Department of Health & Family Welfare"),
    ("HELS/015", "Department of Higher Education and Languages"),
    ("HAJE/016", "Department of Home Affairs and Justice"),
    ("HCTE/017", "Department of Horticulture"),
    ("HUDA/018", "Department of Housing and Urban Development Authority"),
    ("ICRC/019", "Department of Industries and Commerce"),
    ("IPRN/020", "Department of Information and Public Relation"),
    ("PITI/021", "Department of Promotion of Information Technology Industry"),
    ("IPTN/022", "Department of Investment Promotion"),
    ("LABR/023", "Department of Labour"),
    ("LLAR/024", "Department of Legal and Legislative Affairs"),
    ("LOCG/025", "Department of Local Government"),
    ("MERH/026", "Department of Medical Education and Research"),
    ("NRES/027", "Department of New & Renewable Energy Sources"),
    ("NRIA/028", "Department of NRI Affairs"),
    ("PARS/029", "Department of Parliamentary Affairs"),
    ("PESL/030", "Department of Personnel"),
    ("PLAN/031", "Department of Planning"),
    ("POWR/032", "Department of Power"),
    ("PTSY/033", "Department of Printing and Stationery"),
    ("PROI/034", "Department of Program Implementation"),
    ("PUBW/035", "Department of Public Works"),
    ("RRDM/036", "Department of Revenue, Rehabilitation & Disaster Management"),
    ("RDP/037", "Department of Rural Development and Panchayat"),
    ("SCHE/038", "Department of School Education"),
    ("SCTE/039", "Department of Science, Technology & Environment"),
    ("SJEM/040", "Department of Social Justice, Empowerment and Minorities"),
    ("SSWCD/041", "Department of Social Security and Women & Child Development"),
    ("SWC/042", "Department of Soil & Water Conservation"),
    ("SYS/043", "Department of Sports and Youth Services"),
    ("TEIT/044", "Department of Technical Education and Industrial Training"),
    ("TOCA/045", "Department of Tourism and Cultural Affairs"),
    ("TRSP/046", "Department of Transport"),
    ("VIGI/047", "Department of Vigilance"),
    ("WARS/048", "Department of Water Resources"),
    ("WSSN/049", "Department of Water Supply and Sanitation"),
    ("WEFF/050", "Department of Welfare of Freedom Fighters"),
    ("PPCS/051", "Departments of Punjab Prisons and Correctional Services"),
    ("FODP/052", "Department of Food Processing"),
    ("MIGY/053", "Department of Mines and Geology")

]

with app.app_context():

    for code, name in departments:

        exists = Department.query.filter_by(
            code=code
        ).first()

        if not exists:

            department = Department(
                code=code,
                name=name
            )

            db.session.add(department)

    db.session.commit()

    print("All departments added successfully")
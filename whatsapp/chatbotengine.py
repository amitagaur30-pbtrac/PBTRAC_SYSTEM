from datetime import datetime

from whatsapp.session import user_sessions
from whatsapp.whatsappapi import send_text_message

from services.lookup_service import (
    get_departments,
    get_services,
    get_department,
    get_service
)

from services.complaint_service import (
    create_complaint
)

from models.complaint import Complaint


# =====================================================
# COMMON COMMANDS
# =====================================================

COMMANDS = [
    "menu",
    "back",
    "cancel",
    "restart"
]


# =====================================================
# RESET SESSION
# =====================================================

def reset_session(phone):

    if phone in user_sessions:

        del user_sessions[phone]


# =====================================================
# MAIN MENU
# =====================================================

def show_main_menu(phone):

    user_sessions[phone] = {

        "step": "main_menu",

        "data": {}

    }

    send_text_message(

        phone,

        "🇮🇳 Punjab Transparency & Accountability Commission (PBTRAC)\n\n"

        "Welcome.\n\n"

        "Reply with:\n\n"

        "1️⃣ Register Complaint\n"

        "2️⃣ Track Complaint\n"

        "3️⃣ FAQ\n"

        "4️⃣ Contact PBTRAC"

    )


# =====================================================
# PROCESS MESSAGE
# =====================================================

def process_user_message(phone, message):

    message = message.strip()

    lower = message.lower()


    # ---------------------------------------------

    # First Message

    # ---------------------------------------------

    if phone not in user_sessions:

        show_main_menu(phone)

        return


    session = user_sessions[phone]

    step = session["step"]

    data = session["data"]


    # ---------------------------------------------

    # Universal Commands

    # ---------------------------------------------

    if lower == "menu":

        show_main_menu(phone)

        return


    if lower == "restart":

        show_main_menu(phone)

        return


    if lower == "cancel":

        reset_session(phone)

        send_text_message(

            phone,

            "Conversation cancelled.\n\n"

            "Send HI anytime to start again."

        )

        return


    # =================================================

    # MAIN MENU

    # =================================================

    if step == "main_menu":

        if message == "1":

            session["step"] = "awaiting_name"

            send_text_message(

                phone,

                "Please enter Applicant Full Name."

            )

            return


        elif message == "2":

            session["step"] = "awaiting_tracking"

            send_text_message(

                phone,

                "Please enter Complaint Number."

            )

            return


        elif message == "3":

            send_text_message(

                phone,

                "Frequently Asked Questions\n\n"

                "• Complaint can be filed for delay or non-delivery of notified services.\n\n"

                "• Documents can be submitted later.\n\n"

                "Reply MENU to return."

            )

            return


        elif message == "4":

            send_text_message(

                phone,

                "Punjab Transparency & Accountability Commission\n\n"

                "Website:\n"

                "https://pbtrac.punjab.gov.in\n\n"

                "Reply MENU to return."

            )

            return


        else:

            send_text_message(

                phone,

                "Invalid option.\n\n"

                "Reply 1, 2, 3 or 4."

            )

            return


    # =================================================

    # NAME

    # =================================================

    elif step == "awaiting_name":

        data["applicant_name"] = message

        session["step"] = "awaiting_mobile"

        send_text_message(

            phone,

            "Enter Mobile Number."

        )

        return


    # =================================================

    # MOBILE

    # =================================================

    elif step == "awaiting_mobile":

        if len(message) != 10 or not message.isdigit():

            send_text_message(

                phone,

                "Please enter a valid 10 digit mobile number."

            )

            return

        data["mobile"] = message

        session["step"] = "awaiting_email"

        send_text_message(

            phone,

            "Enter Email Address.\n\n"

            "Reply SKIP if not available."

        )

        return


    # =================================================

    # EMAIL

    # =================================================

    elif step == "awaiting_email":

        if lower == "skip":

            data["email"] = None

        else:

            data["email"] = message

        session["step"] = "awaiting_address"

        send_text_message(

            phone,

            "Enter Complete Address."

        )

        return


    # =================================================

    # ADDRESS

    # =================================================

    elif step == "awaiting_address":

        data["address"] = message

        departments = get_departments()

        session["departments"] = departments

        session["step"] = "search_department"

        send_text_message(

            phone,

            "Enter Department Name to search.\n\n"

            "Example:\n"

            "Revenue\n"

            "Health\n"

            "Education"

        )

        return
    # =================================================
    # SEARCH DEPARTMENT
    # =================================================

    elif step == "search_department":

        departments = get_departments()

        matches = []

        keyword = message.lower()

        for dept in departments:

            if keyword in dept.name.lower():

                matches.append(dept)

        if len(matches) == 0:

            send_text_message(

                phone,

                "No matching department found.\n\n"

                "Please enter another department name."

            )

            return

        if len(matches) == 1:

            department = matches[0]

            data["department_id"] = department.id

            data["department_name"] = department.name

            services = get_services(department.id)

            session["services"] = services

            session["step"] = "search_service"

            send_text_message(

                phone,

                f"Department Selected:\n"

                f"{department.name}\n\n"

                f"Now enter Service Name."

            )

            return

        session["department_matches"] = matches

        session["step"] = "select_department"

        text = "Departments Found\n\n"

        for i, dept in enumerate(matches, start=1):

            text += f"{i}. {dept.name}\n"

        text += "\nReply with option number."

        send_text_message(phone, text)

        return


    # =================================================
    # SELECT DEPARTMENT
    # =================================================

    elif step == "select_department":

        if not message.isdigit():

            send_text_message(

                phone,

                "Reply with option number."

            )

            return

        option = int(message)

        matches = session["department_matches"]

        if option < 1 or option > len(matches):

            send_text_message(

                phone,

                "Invalid option."

            )

            return

        department = matches[option - 1]

        data["department_id"] = department.id

        data["department_name"] = department.name

        services = get_services(department.id)

        session["services"] = services

        session["step"] = "search_service"

        send_text_message(

            phone,

            "Enter Service Name."

        )

        return


    # =================================================
    # SEARCH SERVICE
    # =================================================

    elif step == "search_service":

        keyword = message.lower()

        services = session["services"]

        matches = []

        for service in services:

            if keyword in service.service_name.lower():

                matches.append(service)

        if len(matches) == 0:

            send_text_message(

                phone,

                "No matching service found.\n\n"

                "Try again."

            )

            return

        if len(matches) == 1:

            service = matches[0]

            data["service_id"] = service.id

            data["service_name"] = service.service_name

            session["step"] = "awaiting_office"

            send_text_message(

                phone,

                "Enter Office Name."

            )

            return

        session["service_matches"] = matches

        session["step"] = "select_service"

        text = "Matching Services\n\n"

        for i, service in enumerate(matches, start=1):

            text += f"{i}. {service.service_name}\n"

        text += "\nReply with option number."

        send_text_message(

            phone,

            text

        )

        return


    # =================================================
    # SELECT SERVICE
    # =================================================

    elif step == "select_service":

        if not message.isdigit():

            send_text_message(

                phone,

                "Reply with option number."

            )

            return

        option = int(message)

        matches = session["service_matches"]

        if option < 1 or option > len(matches):

            send_text_message(

                phone,

                "Invalid option."

            )

            return

        service = matches[option - 1]

        data["service_id"] = service.id

        data["service_name"] = service.service_name

        session["step"] = "awaiting_office"

        send_text_message(

            phone,

            "Enter Office Name."

        )

        return


    # =================================================
    # OFFICE NAME
    # =================================================

    elif step == "awaiting_office":

        data["office_name"] = message

        session["step"] = "awaiting_application_number"

        send_text_message(

            phone,

            "Enter Application Number."

        )

        return


    # =================================================
    # APPLICATION NUMBER
    # =================================================

    elif step == "awaiting_application_number":

        data["application_number"] = message

        session["step"] = "awaiting_application_date"

        send_text_message(

            phone,

            "Enter Application Date\n\n"

            "Format:\n"

            "DD-MM-YYYY"

        )

        return


    # =================================================
    # APPLICATION DATE
    # =================================================

    elif step == "awaiting_application_date":

        try:

            application_date = datetime.strptime(

                message,

                "%d-%m-%Y"

            ).date()

        except:

            send_text_message(

                phone,

                "Invalid date.\n\n"

                "Use DD-MM-YYYY"

            )

            return

        data["application_date"] = application_date

        session["step"] = "awaiting_grievance"

        send_text_message(

            phone,

            "Describe your grievance."

        )

        return
        # =================================================
    # GRIEVANCE
    # =================================================

    elif step == "awaiting_grievance":

        if len(message.strip()) < 10:

            send_text_message(

                phone,

                "Please describe your grievance in more detail."

            )

            return

        data["grievance"] = message

        session["step"] = "awaiting_relief"

        send_text_message(

            phone,

            "Please enter the Relief Sought."

        )

        return


    # =================================================
    # RELIEF SOUGHT
    # =================================================

    elif step == "awaiting_relief":

        if len(message.strip()) < 5:

            send_text_message(

                phone,

                "Please enter the relief sought."

            )

            return

        data["relief_sought"] = message

        session["step"] = "confirm_submission"

        summary = (

            "📋 *Please confirm your complaint details*\n\n"

            f"👤 Name: {data['applicant_name']}\n"

            f"📱 Mobile: {data['mobile']}\n"

            f"📧 Email: {data['email'] if data['email'] else 'Not Provided'}\n"

            f"🏠 Address: {data['address']}\n\n"

            f"🏢 Department: {data['department_name']}\n"

            f"📄 Service: {data['service_name']}\n"

            f"🏛 Office: {data['office_name']}\n\n"

            f"🆔 Application No: {data['application_number']}\n"

            f"📅 Application Date: {data['application_date'].strftime('%d-%m-%Y')}\n\n"

            f"📝 Grievance:\n{data['grievance']}\n\n"

            f"🎯 Relief Sought:\n{data['relief_sought']}\n\n"

            "Reply:\n"

            "1 - Submit Complaint\n"

            "2 - Cancel"

        )

        send_text_message(

            phone,

            summary

        )

        return


    # =================================================
    # CONFIRM SUBMISSION
    # =================================================

    elif step == "confirm_submission":

        if message == "2":

            reset_session(phone)

            send_text_message(

                phone,

                "Complaint registration cancelled."

            )

            return


        if message != "1":

            send_text_message(

                phone,

                "Reply with:\n"

                "1 - Submit Complaint\n"

                "2 - Cancel"

            )

            return


        complaint = create_complaint(

            applicant_name=data["applicant_name"],

            mobile=data["mobile"],

            email=data["email"],

            address=data["address"],

            office_name=data["office_name"],

            department_id=data["department_id"],

            service_id=data["service_id"],

            application_number=data["application_number"],

            application_date=data["application_date"],

            grievance=data["grievance"],

            relief_sought=data["relief_sought"]

        )

        session["complaint_no"] = complaint.complaint_no

        session["step"] = "registration_complete"

        send_text_message(

            phone,

            "✅ Complaint Registered Successfully.\n\n"

            f"Complaint Number:\n"

            f"{complaint.complaint_no}\n\n"

            "Please save this Complaint Number for future reference.\n\n"

            "Reply MENU for Main Menu."

        )

        return


    # =================================================
    # REGISTRATION COMPLETE
    # =================================================

    elif step == "registration_complete":

        reset_session(phone)

        show_main_menu(phone)

        return
        # =================================================
    # TRACK COMPLAINT
    # =================================================

    elif step == "awaiting_tracking":

        complaint = Complaint.query.filter_by(

            complaint_no=message.strip().upper()

        ).first()

        if complaint:

            department = get_department(
                complaint.department_id
            )

            service = get_service(
                complaint.service_id
            )

            reply = (

                "📋 Complaint Details\n\n"

                f"Complaint No:\n"
                f"{complaint.complaint_no}\n\n"

                f"Applicant:\n"
                f"{complaint.applicant_name}\n\n"

                f"Department:\n"
                f"{department.name if department else '-'}\n\n"

                f"Service:\n"
                f"{service.service_name if service else '-'}\n\n"

                f"Status:\n"
                f"{complaint.status}\n\n"

                f"Remarks:\n"
                f"{complaint.remarks if complaint.remarks else 'No remarks available.'}"

            )

            send_text_message(
                phone,
                reply
            )

        else:

            send_text_message(

                phone,

                "❌ Complaint not found.\n\n"

                "Please check your Complaint Number and try again."

            )

        reset_session(phone)

        show_main_menu(phone)

        return


    # =================================================
    # FALLBACK
    # =================================================

    else:

        send_text_message(

            phone,

            "Invalid input.\n\n"

            "Reply MENU to return to Main Menu."

        )

        return
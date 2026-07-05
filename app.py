import os
from database.initialize_database import initialize_database
from flask import Flask, render_template

from database.db import db

from routes.citizen import citizen_bp
from routes.admin import admin_bp

# WhatsApp Blueprint
from whatsapp.webhook import whatsapp_bp

app = Flask(__name__)

# ==================================================
# CONFIGURATION
# ==================================================

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ptac.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "ptac_secret_key"
)

# ==================================================
# DATABASE INITIALIZATION
# ==================================================

db.init_app(app)

with app.app_context():

    from models.complaint import Complaint
    from models.admin import Admin
    from models.department import Department
    from models.service import Service
    from models.document import ComplaintDocument

    db.create_all()

    initialize_database()
# ==================================================
# REGISTER BLUEPRINTS
# ==================================================

app.register_blueprint(
    citizen_bp
)

app.register_blueprint(
    admin_bp
)

app.register_blueprint(
    whatsapp_bp
)

# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def home():

    return render_template(
        "home.html"
    )


# ==================================================
# FAQ PAGE
# ==================================================

@app.route("/faq")
def faq():

    return render_template(
        "faq.html"
    )


# ==================================================
# DEBUG ROUTES
# ==================================================

print("\nRegistered Routes:\n")
print(app.url_map)

# ==================================================
# RUN APPLICATION
# ==================================================

import os

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )   
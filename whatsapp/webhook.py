from flask import Blueprint
from flask import request

from whatsapp.messagehandler import handle_message

whatsapp_bp = Blueprint(
    "whatsapp",
    __name__
)

VERIFY_TOKEN = "ptac_verify"


@whatsapp_bp.route(
    "/webhook",
    methods=["GET", "POST"]
)
def webhook():

    # Meta verification

    if request.method == "GET":

        mode = request.args.get(
            "hub.mode"
        )

        token = request.args.get(
            "hub.verify_token"
        )

        challenge = request.args.get(
            "hub.challenge"
        )

        if (
            mode == "subscribe"
            and token == VERIFY_TOKEN
        ):

            return challenge, 200

        return "Verification failed", 403

    # Receive messages

    if request.method == "POST":

        data = request.get_json()

        print("\nIncoming WhatsApp Message:")
        print(data)

        handle_message(data)

        return "OK", 200
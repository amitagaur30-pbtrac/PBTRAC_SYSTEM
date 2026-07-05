from whatsapp.chatbotengine import process_user_message


def handle_message(data):

    print("Incoming data received")

    try:

        message = (
            data["entry"][0]
            ["changes"][0]
            ["value"]
            ["messages"][0]
        )

        sender = message["from"]

        message_type = message.get(
            "type"
        )

        print("Sender:", sender)

        # Text message

        if message_type == "text":

            text = message[
                "text"
            ]["body"]

            print("Message:", text)

            process_user_message(
                sender,
                text
            )

        else:

            print(
                "Unsupported message type:",
                message_type
            )

    except Exception as e:

        print(
            "Error processing message:",
            e
        )
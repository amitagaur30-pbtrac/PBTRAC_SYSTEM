import requests

#ACCESS_TOKEN = "07b0bed57934afc949686c59f0eca93b"

#PHONE_NUMBER_ID = "1243234338866518"
ACCESS_TOKEN = "YOUR_WHATSAPP_ACCESS_TOKEN"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"

def send_text_message(phone, message):

    url = (
        f"https://graph.facebook.com/v25.0/"
        f"{PHONE_NUMBER_ID}/messages"
    )

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {
            "body": message
        }
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=20
        )

        print("\n===== WhatsApp API =====")
        print("Status:", response.status_code)
        print(response.text)
        print("========================\n")

    except Exception as e:

        print("WhatsApp API Error:", e)

    print("Status:", response.status_code)
    print("Response:", response.text)

import requests
import os


from dotenv import load_dotenv

load_dotenv()


WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def webhook(payload: dict):

    try:

        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            timeout=5
        )

        print(f"[WEBHOOK] Sent with status {response.status_code}")

    except Exception as error:

        print(f"[WEBHOOK ERROR] {error}")
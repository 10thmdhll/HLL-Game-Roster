import requests
import config

def send_to_discord(image_path):
    url = config.DISCORD_WEBHOOK_URL
    if not url:
        print("No webhook URL configured.")
        return

    with open(image_path, "rb") as f:
        files = {"file": ("poster.png", f)}
        data = {
            "content": "Here is the event roster.",
            "username": "HLL Bot"
        }
        response = requests.post(url, data=data, files=files)

    if response.status_code != 204 and response.status_code != 200:
        print(f"Failed to send to Discord: {response.status_code} - {response.text}")

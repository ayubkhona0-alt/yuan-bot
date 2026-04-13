import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = "@beshsomm"

def get_cny_rate():
    url = "https://open.er-api.com/v6/latest/CNY"
    data = requests.get(url).json()
    return data["rates"]["UZS"]

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text
    }
    requests.post(url, data=payload)

def main():
    rate = get_cny_rate()
    text = f"💴 Курс юаня\n\n1 CNY = {rate} UZS"
    send_message(text)

if __name__ == "__main__":
    main()

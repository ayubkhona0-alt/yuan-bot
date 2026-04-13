import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = "@beshsomm"

def get_rate():
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
    today_rate = get_rate()

    # Простая логика изменения (пример)
    change = round(today_rate - 1770, 2)

    if change > 0:
        trend = "📈 Рост"
    elif change < 0:
        trend = "📉 Падение"
    else:
        trend = "➖ Без изменений"

    text = f"""💴 Курс юаня (CNY)

📊 Сегодня: {today_rate} UZS
{trend}: {change} UZS

📦 Китай → Узбекистан
🚚 Доставка 13–16 дней

👉 @beshsomm
"""

    send_message(text)

if name == "__main__":
    main()

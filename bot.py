import os
import json
from datetime import datetime
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = "@beshsomm"
DATA_FILE = "rates.json"


def get_rates():
    url = "https://open.er-api.com/v6/latest/USD"
    usd_data = requests.get(url, timeout=20).json()

    usd_to_uzs = round(usd_data["rates"]["UZS"])
    updated = usd_data.get("time_last_update_utc", "")

    cny_to_usd = usd_data["rates"]["CNY"]
    cny_to_uzs = round(usd_to_uzs / cny_to_usd)

    return {
        "USD": usd_to_uzs,
        "CNY": cny_to_uzs,
        "updated": updated
    }


def load_previous_rates():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def save_rates(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def format_change(today, yesterday):
    if yesterday is None:
        return "➖ Нет данных"

    diff = today - yesterday

    if diff > 0:
        return f"📈 +{diff}"
    if diff < 0:
        return f"📉 {diff}"
    return "➖ 0"


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text
    }
    r = requests.post(url, data=payload, timeout=20)
    r.raise_for_status()


def main():
    current = get_rates()
    previous = load_previous_rates()

    cny_change = format_change(
        current["CNY"],
        previous["CNY"] if previous else None
    )
    usd_change = format_change(
        current["USD"],
        previous["USD"] if previous else None
    )

    today_date = datetime.now().strftime("%d.%m.%Y")

    text = f"""💱 Курс валют на {today_date}

🇨🇳 Юань:
1 CNY = {current["CNY"]} UZS
Изменение: {cny_change}

🇺🇸 Доллар:
1 USD = {current["USD"]} UZS
Изменение: {usd_change}

📦 Китай → Узбекистан
🚚 Доставка 13–16 дней

👉 @beshsomm"""

    send_message(text)
    save_rates(current)


if __name__ == "__main__":
    main()

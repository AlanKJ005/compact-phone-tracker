import os
import re
import requests
import pandas as pd

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def send_telegram(msg):
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )
    print(response.text)

def get_price(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        html = r.text

        # Find common ₹ prices in page source
        matches = re.findall(r'₹\s?([\d,]+)', html)

        if not matches:
            return None

        prices = []

        for p in matches:
            try:
                prices.append(int(p.replace(",", "")))
            except:
                pass

        if not prices:
            return None

        # Usually current price is among the smallest visible prices
        return min(prices)

    except Exception as e:
        print(f"ERROR: {e}")
        return None


phones = pd.read_csv("phones.csv")

for _, row in phones.iterrows():

    name = row["name"]
    target = int(row["target_price"])
    url = row["url"]

    print(f"\nChecking {name}")

    price = get_price(url)

    print(f"Detected price: {price}")

    if price is None:
        continue

    if price <= target:

        msg = (
            f"📱 DEAL FOUND\n\n"
            f"{name}\n"
            f"Current Price: ₹{price:,}\n"
            f"Target Price: ₹{target:,}\n\n"
            f"{url}"
        )

        send_telegram(msg)

import os
import requests
import pandas as pd

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

def get_price(model):
    """
    Replace this function with your chosen data source.

    Must return:
        int price
    or
        None
    """

    return None

phones = pd.read_csv("phones.csv")

for _, row in phones.iterrows():

    model = row["model"]
    target = int(row["target_price"])

    price = get_price(model)

    if price is None:
        continue

    if price <= target:

        message = (
            f"📱 COMPACT PHONE ALERT\n\n"
            f"{model}\n"
            f"Price: ₹{price:,}\n"
            f"Target: ₹{target:,}"
        )

        send_telegram(message)
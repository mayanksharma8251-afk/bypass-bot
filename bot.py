import os
import json
import requests
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
app = Flask(__name__)

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    requests.post(url, json=payload)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return "OK", 200

    message = data.get("message")
    if not message:
        return "OK", 200

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        send_message(chat_id,
            "❤️ SHORTNER BYPASS BOT BY @CLASSYNETWORK\n\n"
            "Send /skip <link> to bypass any shortened URL."
        )
    elif text.startswith("/skip"):
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            send_message(chat_id, "❌ Please provide a link.\nExample: /skip https://bit.ly/xyz123")
            return "OK", 200

        short_url = parts[1]
        send_message(chat_id, "⏳ Processing... (may take 20-30 seconds)")

        # Temporary result (add real bypass logic later)
        result = f"Bypassed: {short_url}"

        send_message(chat_id,
            f"❤️ Original Link :✅ {short_url}\n"
            f"Bypassed Link :✅ {result}\n"
            f"─────────────────\n"
            f"Powered By @CLASSYNETWORK"
        )

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

import os
import re
import requests
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
app = Flask(__name__)

def bypass_link(short_url):
    try:
        # Try bypass.pm API
        response = requests.get(
            f"https://bypass.pm/api/bypass?url={short_url}",
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("bypassed") or data.get("url") or data.get("result") or "❌ No URL found"
        else:
            return f"❌ Error: {response.status_code}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

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

    # /start command
    if text == "/start":
        send_message(chat_id,
            "❤️ SHORTNER BYPASS BOT BY @CLASSYNETWORK\n\n"
            "Simply send me any shortened link.\n"
            "Example: https://bit.ly/xyz123\n\n"
            "I'll bypass it instantly!"
        )
        return "OK", 200

    # DIRECT LINK — NO /skip COMMAND
    if re.match(r'^https?://', text):
        send_message(chat_id, "⏳ Processing your link... (may take 10-15 seconds)")
        result = bypass_link(text)
        send_message(chat_id,
            f"❤️ Original Link :✅ {text}\n"
            f"Bypassed Link :✅ {result}\n"
            f"─────────────────\n"
            f"Powered By @CLASSYNETWORK"
        )
    else:
        send_message(chat_id, "❌ Please send a valid URL starting with http:// or https://")

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

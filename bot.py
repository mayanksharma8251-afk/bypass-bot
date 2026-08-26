import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from flask import Flask, request
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
app = Flask(__name__)

def bypass_with_browser(short_url):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.binary_location = "/usr/bin/google-chrome"

        driver = webdriver.Chrome(options=options)

        driver.get("https://adskip.sryze.cc")

        input_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
        )
        input_field.send_keys(short_url)

        bypass_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Bypass')]")
        bypass_btn.click()

        result_elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'result')]//a"))
        )
        bypassed_url = result_elem.get_attribute("href")
        driver.quit()
        return bypassed_url

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
        send_message(chat_id, "⏳ Processing... (may take 30-45 seconds)")

        result = bypass_with_browser(short_url)

        send_message(chat_id,
            f"❤️ Original Link :✅ {short_url}\n"
            f"Bypassed Link :✅ {result}\n"
            f"─────────────────\n"
            f"Powered By @CLASSYNETWORK"
        )

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

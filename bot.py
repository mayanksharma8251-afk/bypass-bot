import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❤️ SHORTNER BYPASS BOT BY @CLASSYNETWORK\n\n"
        "Send /skip <link> to bypass any shortened URL."
    )

async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide a link.\nExample: /skip https://bit.ly/xyz123")
        return
    short_url = context.args[0]
    await update.message.reply_text("⏳ Processing... (20-30 seconds)")
    result = bypass_with_browser(short_url)
    await update.message.reply_text(
        f"❤️ Original Link :✅ {short_url}\n"
        f"Bypassed Link :✅ {result}\n"
        f"─────────────────\n"
        f"Powered By @CLASSYNETWORK"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("skip", skip))
    print("✅ Bot is running on Render...")
    app.run_polling()

if __name__ == "__main__":
    main()

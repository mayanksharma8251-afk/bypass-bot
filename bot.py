import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "❤️ SHORTNER BYPASS BOT BY @CLASSYNETWORK\n\n"
        "Send /skip <link> to bypass any shortened URL."
    )

def skip(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("❌ Please provide a link.\nExample: /skip https://bit.ly/xyz123")
        return
    short_url = context.args[0]
    update.message.reply_text("⏳ Processing... (may take 20-30 seconds)")

    # Temporary result (replace with actual bypass logic later)
    result = f"Bypassed: {short_url}"

    update.message.reply_text(
        f"❤️ Original Link :✅ {short_url}\n"
        f"Bypassed Link :✅ {result}\n"
        f"─────────────────\n"
        f"Powered By @CLASSYNETWORK"
    )

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("skip", skip))
    print("✅ Bot is running on Render...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

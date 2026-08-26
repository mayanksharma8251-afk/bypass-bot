import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

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
    await update.message.reply_text("⏳ Processing... (may take 20-30 seconds)")

    # Simulate bypass (replace with actual logic later)
    result = f"Bypassed: {short_url}"  # temporary

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

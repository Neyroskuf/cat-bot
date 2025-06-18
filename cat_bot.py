from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import urllib.parse
import time

BOT_TOKEN = "7885828113:AAEx4T2WTh3B0ondFCAsOn5vmoXnLPcST-g"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я котобот 🐱\n"
        "/cat — случайный кот\n"
        "/cat Привет — кот с подписью"
    )

async def send_cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        timestamp = int(time.time())
        if context.args:
            text = urllib.parse.quote(" ".join(context.args))
            cat_url = f"https://cataas.com/cat/says/{text}?size=50&timestamp={timestamp}"
        else:
            cat_url = f"https://cataas.com/cat?timestamp={timestamp}"

        await update.message.reply_photo(cat_url)

    except Exception as e:
        await update.message.reply_text("😿 Не удалось получить котика...")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cat", send_cat))
    app.run_polling()
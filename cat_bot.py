from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import urllib.parse
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

BOT_TOKEN = "7885828113:AAEx4T2WTh3B0ondFCAsOn5vmoXnLPcST-g"

# Команды бота
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

# Фейковый HTTP-сервер для Render (чтобы не вырубало Web Service)
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_dummy_server():
    server = HTTPServer(('0.0.0.0', 10000), DummyHandler)
    server.serve_forever()

if __name__ == "__main__":
    # Запускаем HTTP-сервер в отдельном потоке
    threading.Thread(target=run_dummy_server, daemon=True).start()

    # Запускаем Telegram-бота
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cat", send_cat))
    app.run_polling()

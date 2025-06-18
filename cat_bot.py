from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import urllib.parse
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import asyncio

BOT_TOKEN = "7885828113:AAEx4T2WTh3B0ondFCAsOn5vmoXnLPcST-g"  # Вставь сюда токен от BotFather

# HTTP-сервер для Render, чтобы сессия не падала
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_dummy_server():
    server = HTTPServer(("0.0.0.0", 10000), DummyHandler)
    server.serve_forever()

# Команды Telegram-бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[start] От {update.effective_user.username}")
    await update.message.reply_text("Привет! Я котобот 🐱\n/cat — случайный кот\n/cat Привет — кот с подписью")

async def send_cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        timestamp = int(time.time())
        if context.args:
            text = urllib.parse.quote(" ".join(context.args))
            cat_url = f"https://cataas.com/cat/says/{text}?size=50&timestamp={timestamp}"
        else:
            cat_url = f"https://cataas.com/cat?timestamp={timestamp}"
        print(f"[cat] Отправка: {cat_url}")
        await update.message.reply_photo(cat_url)
    except Exception as e:
        print("Ошибка отправки кота:", e)
        await update.message.reply_text("😿 Не удалось получить котика...")

async def log_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[log] Сообщение: {update.message.text}")

# Пульс бота
async def heartbeat():
    while True:
        print("[pulse] Бот активен:", time.strftime("%Y-%m-%d %H:%M:%S"))
        await asyncio.sleep(30)

async def main():
    # Запускаем фейковый сервер в отдельном потоке
    threading.Thread(target=run_dummy_server, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cat", send_cat))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_all))

    # Запускаем пульс параллельно с polling
    asyncio.create_task(heartbeat())
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

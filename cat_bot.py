import asyncio
import time
import urllib.parse
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "7885828113:AAEx4T2WTh3B0ondFCAsOn5vmoXnLPcST-g"

# HTTP-сервер для Render, чтобы не завершался сервис
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_dummy_server():
    server = HTTPServer(('0.0.0.0', 10000), DummyHandler)
    server.serve_forever()

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[start] @{user.username} ({user.id})")
    await update.message.reply_text(
        "Привет! Я котобот 🐱\n"
        "/cat — случайный кот\n"
        "/cat Привет — кот с подписью\n"
        "/ping — проверить, жив ли я"
    )

async def send_cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        timestamp = int(time.time())
        if context.args:
            text = urllib.parse.quote(" ".join(context.args))
            cat_url = f"https://cataas.com/cat/says/{text}?size=50&timestamp={timestamp}"
        else:
            cat_url = f"https://cataas.com/cat?timestamp={timestamp}"

        print(f"[cat] @{user.username} ({user.id}) → {cat_url}")
        await update.message.reply_photo(cat_url)

    except Exception as e:
        print(f"❌ Ошибка для @{user.username} ({user.id}): {e}")
        await update.message.reply_text("😿 Не удалось получить котика...")

# Пинг — ручная проверка работоспособности
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[ping] @{user.username} ({user.id}) отправил ping")
    await update.message.reply_text("✅ Я на месте!")

# Лог всех текстов
async def log_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message.text
    print(f"[log] @{user.username} ({user.id}): {msg}")

# Пульс
async def heartbeat():
    while True:
        print(f"[pulse] Бот активен: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        await asyncio.sleep(30)

# Асинхронный запуск
async def main():
    threading.Thread(target=run_dummy_server, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cat", send_cat))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_all))

    asyncio.create_task(heartbeat())
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

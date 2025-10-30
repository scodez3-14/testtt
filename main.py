import os
from flask import Flask, request, jsonify
import requests

BOT_TOKEN = "8409213603:AAFaJfxhdFpmP3yGbBzbtoPpHd8I9SizxNU"
if not BOT_TOKEN:
    raise RuntimeError("❌ Please set BOT_TOKEN environment variable")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/"

app = Flask(__name__)

# --- Telegram helper ---
def send_message(chat_id, text):
    url = TELEGRAM_API + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)

# --- Webhook route ---
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # Simple response
        send_message(chat_id, "Hi there! 👋")

    return jsonify(ok=True)

# --- Health check ---
@app.route("/", methods=["GET"])
def home():
    return "Bot is alive ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

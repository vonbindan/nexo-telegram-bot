from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8616825736:AAHbO2V3ME1mVbJXsGCUQWXwCvrYFm7rWhc")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "810066278")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=data)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        if data and "text" in data:
            send_telegram(data["text"])
        else:
            body = request.data.decode("utf-8")
            if body:
                send_telegram(body)
    except Exception as e:
        send_telegram(f"Ошибка: {str(e)}")
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "NEXO Signal Bot is running!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

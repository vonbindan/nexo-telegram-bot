from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8616825736:AAHbO2V3ME1mVbJXsGCUQWXwCvrYFm7rWhc")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "-5005918558")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram error: {e}")

@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    try:
        data = request.get_json(force=True, silent=True)
        if data and isinstance(data, dict) and "text" in data:
            send_telegram(data["text"])
            return "OK", 200

        body = request.data.decode("utf-8").strip()
        if body:
            send_telegram(body)
            return "OK", 200

        form_text = request.form.get("text", "")
        if form_text:
            send_telegram(form_text)
            return "OK", 200

        send_telegram("Сигнал получен")
        return "OK", 200

    except Exception as e:
        print(f"Error: {e}")
        return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "NEXO Signal Bot is running!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

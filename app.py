import os
import json
import hashlib
import hmac
import requests
from flask import Flask, render_template, request, redirect, url_for
from twilio.rest import Client

app = Flask(__name__)

# Ortam değişkenleri (Render üzerinde ayarla)
SHOPIER_API_KEY = os.getenv("SHOPIER_API_KEY")
SHOPIER_SECRET_KEY = os.getenv("SHOPIER_SECRET_KEY")
SHOPIER_API_URL = "https://api.shopier.com/v1/checkout/create"

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
ADMIN_NUMBERS = os.getenv("ADMIN_NUMBERS", "+905055719417").split(",")
client = Client(TWILIO_SID, TWILIO_TOKEN)

games = ["Valorant", "CS2", "LoL", "Apex"]
packages = [
    {"name": "Basit", "price_tl": 660},
    {"name": "Orta", "price_tl": 880},
    {"name": "Pro", "price_tl": 1150},
    {"name": "Oyun Ustasi", "price_tl": 1560}
]
feedbacks = []

def create_zoom_link():
    return "https://zoom.us/j/" + os.urandom(4).hex()

def notify_admins(game, pkg, time, zoom_link):
    msg = f"\U0001F3AE Oyun: {game}\n\U0001F4E6 Paket: {pkg}\n\u23F0 Saat: {time}\n\U0001F517 Zoom: {zoom_link}"
    for admin in ADMIN_NUMBERS:
        client.messages.create(
            body=msg,
            from_='whatsapp:' + TWILIO_WHATSAPP_NUMBER,
            to='whatsapp:' + admin.strip()
        )

@app.route("/")
def index():
    return render_template("index.html", games=games, packages=packages, feedbacks=feedbacks)

@app.route("/checkout", methods=["POST"])
def checkout():
    game = request.form.get("game")
    pkg = request.form.get("package")
    time = request.form.get("time")

    package = next((p for p in packages if p["name"] == pkg), None)
    if not game or not package or not time:
        return render_template("error.html", message="Eksik bilgi girdiniz."), 400

    # Shopier için ödeme verisi hazırla
    price = package["price_tl"]
    order_id = os.urandom(6).hex()
    callback_url = url_for('payment_result', _external=True)

    # Shopier API'ye gönderilecek veri (örnek)
    data = {
        "api_key": SHOPIER_API_KEY,
        "order_id": order_id,
        "price": price,
        "currency": "TRY",
        "callback_url": callback_url,
        "description": f"{game} - {pkg} paket - {time}",
        "customer_email": request.form.get("email", ""),  # opsiyonel
        "customer_name": request.form.get("name", ""),    # opsiyonel
    }

    # Shopier API imza hesaplama (örnek, Shopier dökümantasyonuna göre değişebilir)
    def generate_signature(params, secret):
        sorted_items = sorted(params.items())
        base_string = "".join(f"{k}{v}" for k, v in sorted_items)
        return hmac.new(secret.encode(), base_string.encode(), hashlib.sha256).hexdigest()

    signature = generate_signature(data, SHOPIER_SECRET_KEY)
    data["signature"] = signature

    # Shopier ödeme linkini al
    try:
        response = requests.post(SHOPIER_API_URL, json=data)
        response.raise_for_status()
        res_json = response.json()
        if res_json.get("status") == "success":
            payment_url = res_json.get("payment_url")
            # Zoom linki ve admin bildirimi ödeme sonrası yapılabilir
            return redirect(payment_url)
        else:
            return render_template("error.html", message="Ödeme başlatılamadı: " + res_json.get("message", "Bilinmeyen hata")), 400
    except Exception as e:
        return render_template("error.html", message="Ödeme isteği başarısız: " + str(e)), 500

@app.route("/payment-result", methods=["POST", "GET"])
def payment_result():
    # Shopier ödeme sonucu genellikle webhook olarak gelir, ya da redirect ile parametreler
    # Burada parametre kontrolü yapabilirsin
    status = request.args.get("status")
    order_id = request.args.get("order_id")

    if status == "success":
        zoom_link = create_zoom_link()
        # Bildirim ve diğer işlemler
        # Örnek: notify_admins() çağırabilirsin (ama order_id vs parametrelerle)
        notify_admins("Bilinmeyen Oyun", "Bilinmeyen Paket", "Bilinmeyen Saat", zoom_link)
        return render_template("success.html", zoom_link=zoom_link)
    else:
        return render_template("cancel.html", error="Ödeme başarısız veya iptal edildi.")

@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    comment = request.form.get("comment")
    if comment:
        feedbacks.append(comment)
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

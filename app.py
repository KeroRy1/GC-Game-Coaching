import os
from flask import Flask, render_template, request, redirect, url_for, flash
import hashlib
import hmac
import base64
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Shopier bilgileri
SHOPIER_API_KEY = 'YOUR_API_KEY'
SHOPIER_API_SECRET = 'YOUR_API_SECRET'
SHOPIER_URL = 'https://www.shopier.com/ShowProduct/api_pay4.php'

# Paketler
packages = {
    "ekonomik": {
        "name": "Ekonomik Paket",
        "price": 1000,
        "levels": ["Basit", "Orta"]
    },
    "normal": {
        "name": "Normal Paket",
        "price": 1500,
        "levels": ["Basit", "Orta", "Pro", "Oyun Ustası"]
    }
}

# Tekil seviyeler
individual_levels = {
    "Basit": 400,
    "Orta": 500,
    "Pro": 600,
    "Oyun Ustası": 650
}

# Basit geri bildirim deposu
feedbacks = []

@app.route('/')
def index():
    return render_template("index.html", packages=packages, levels=individual_levels, feedbacks=feedbacks)

@app.route('/buy/<package_key>')
def buy_package(package_key):
    if package_key not in packages:
        flash("Geçersiz paket.", "danger")
        return redirect(url_for('index'))

    package = packages[package_key]
    order_id = str(uuid.uuid4())

    data = f"{SHOPIER_API_KEY}{order_id}"
    signature = base64.b64encode(hmac.new(SHOPIER_API_SECRET.encode(), data.encode(), hashlib.sha256).digest()).decode()

    return render_template("pay.html", shopier_url=SHOPIER_URL,
                           order_id=order_id,
                           product_name=package["name"],
                           price=package["price"],
                           api_key=SHOPIER_API_KEY,
                           signature=signature,
                           buyer_name="Kerem",
                           buyer_surname="Karaman",
                           buyer_email="mail@example.com")

@app.route('/buy-level/<level>')
def buy_level(level):
    if level not in individual_levels:
        flash("Geçersiz seviye.", "danger")
        return redirect(url_for('index'))

    price = individual_levels[level]
    order_id = str(uuid.uuid4())

    data = f"{SHOPIER_API_KEY}{order_id}"
    signature = base64.b64encode(hmac.new(SHOPIER_API_SECRET.encode(), data.encode(), hashlib.sha256).digest()).decode()

    return render_template("pay.html", shopier_url=SHOPIER_URL,
                           order_id=order_id,
                           product_name=level,
                           price=price,
                           api_key=SHOPIER_API_KEY,
                           signature=signature,
                           buyer_name="Kerem",
                           buyer_surname="Karaman",
                           buyer_email="mail@example.com")

@app.route('/feedback', methods=['POST'])
def feedback():
    text = request.form.get("feedback")
    if text:
        feedbacks.append(text)
        flash("Geri bildiriminiz için teşekkür ederiz!", "success")
    return redirect(url_for("index"))

@app.route('/shopier_callback', methods=['POST'])
def shopier_callback():
    order_id = request.form.get("platform_order_id")
    flash("Ödeme alındı. Teşekkürler!", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

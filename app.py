import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import hashlib
import hmac
import base64
import uuid
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Shopier Ayarları
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

@app.route('/')
def index():
    return render_template('index.html', packages=packages)

@app.route('/buy/<package_key>', methods=['GET'])
def buy(package_key):
    if package_key not in packages:
        flash("Geçersiz paket.", "danger")
        return redirect(url_for('index'))

    package = packages[package_key]

    # Shopier parametreleri
    order_id = str(uuid.uuid4())
    buyer_name = "Kerem"
    buyer_surname = "Karaman"
    buyer_email = "mail@example.com"

    # Sign oluşturma
    data = f"{SHOPIER_API_KEY}{order_id}"
    signature = base64.b64encode(hmac.new(SHOPIER_API_SECRET.encode(), data.encode(), hashlib.sha256).digest()).decode()

    return render_template("pay.html", 
                           shopier_url=SHOPIER_URL,
                           order_id=order_id,
                           package=package,
                           api_key=SHOPIER_API_KEY,
                           signature=signature,
                           buyer_name=buyer_name,
                           buyer_surname=buyer_surname,
                           buyer_email=buyer_email)

@app.route('/shopier_callback', methods=['POST'])
def shopier_callback():
    # Shopier'den gelen verilerle doğrulama yapılabilir
    order_id = request.form.get("platform_order_id")
    # Burada ödeme doğrulama yapılmalı (güvenlik için Shopier IP kontrolü vs.)
    flash("Ödeme başarıyla alındı.", "success")
    return redirect(url_for('index'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

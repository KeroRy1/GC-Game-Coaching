import os
from flask import Flask, render_template, request, redirect, url_for, flash
import hashlib
import hmac
import base64
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Shopier bilgileri (bunları kendi bilgilerinle değiştir)
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

# Oyunlar
games = ["Apex", "Valorant", "LoL", "CS2"]

# Saatler 8-19 (tekil seviyeler için)
hours = list(range(8, 20))

# Geri bildirim listesi
feedbacks = []

# Kullanıcıların satın aldıkları paket ve başlangıç tarihleri
# Basit örnek olarak, gerçek projede veritabanı olmalı
user_packages = {}

@app.route('/')
def index():
    return render_template("index.html", packages=packages, levels=individual_levels,
                           feedbacks=feedbacks, games=games, hours=hours)

@app.route('/individual')
def individual():
    return render_template("individual.html", levels=individual_levels, games=games, hours=hours)

@app.route('/buy', methods=['POST'])
def buy():
    package_key = request.form.get('package_key')
    game = request.form.get('game')

    if package_key not in packages or game not in games:
        flash("Geçersiz paket veya oyun seçimi.", "danger")
        return redirect(url_for('index'))

    # Saat kontrolü: şimdi saat 19:00'dan sonrası ise uyarı ver
    now_hour = datetime.now().hour
    if now_hour >= 19:
        flash("Saat 19:00'dan sonra paket satın alma mümkün değil. Lütfen 08:00-19:00 arası tekrar deneyin.", "warning")
        return redirect(url_for('index'))

    package = packages[package_key]
    order_id = str(uuid.uuid4())

    data = f"{SHOPIER_API_KEY}{order_id}"
    signature = base64.b64encode(hmac.new(SHOPIER_API_SECRET.encode(), data.encode(), hashlib.sha256).digest()).decode()

    product_name = f"{package['name']} - {game}"

    # Burada kullanıcıya paket satın alma tarihi atıyoruz (örnek, kullanıcı id yok ama varsayıyoruz 'user1')
    # Gerçek projede kullanıcı id veya session ile yönetilecek
    user_packages['user1'] = {
        'package': package_key,
        'start_date': datetime.now(),
        'valid_until': datetime.now() + timedelta(days=30)
    }

    return render_template("pay.html", shopier_url=SHOPIER_URL,
                           order_id=order_id,
                           product_name=product_name,
                           price=package["price"],
                           api_key=SHOPIER_API_KEY,
                           signature=signature,
                           buyer_name="Kerem",
                           buyer_surname="Karaman",
                           buyer_email="mail@example.com")

@app.route('/buy-level', methods=['POST'])
def buy_level():
    level = request.form.get('level')
    game = request.form.get('game')
    hour = request.form.get('hour')

    if level not in individual_levels or game not in games or not hour or not hour.isdigit() or int(hour) not in hours:
        flash("Geçersiz seviye, oyun veya saat seçimi.", "danger")
        return redirect(url_for('individual'))

    price = individual_levels[level]
    order_id = str(uuid.uuid4())

    data = f"{SHOPIER_API_KEY}{order_id}"
    signature = base64.b64encode(hmac.new(SHOPIER_API_SECRET.encode(), data.encode(), hashlib.sha256).digest()).decode()

    product_name = f"{level} - {game} - Saat: {hour}:00"

    return render_template("pay.html", shopier_url=SHOPIER_URL,
                           order_id=order_id,
                           product_name=product_name,
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


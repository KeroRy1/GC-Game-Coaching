from flask import Flask, render_template, request, jsonify
from models.db import get_available_coach, update_purchase_status, save_purchase
from utils.shopier_webhook import verify_shopier_signature
from utils.whatsapp_notifier import notify_coaches
from utils.zoom import create_zoom_link
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/purchase', methods=["POST"])
def purchase():
    # Kullanıcının seçimlerini al
    game = request.form.get("game")
    level = request.form.get("level")
    time = request.form.get("time")

    # Satın alma kaydı veritabanına işlenir (ödeme bekleniyor)
    purchase_id = save_purchase(game, level, time)
    
    # Shopier yönlendirmesi yapılır (örnek URL yerine gerçek dinamik link kullanılmalı)
    return render_template("success.html", message="Ödeme sayfasına yönlendirileceksiniz.")

@app.route('/shopier-webhook', methods=["POST"])
def shopier_webhook():
    if not verify_shopier_signature(request.form):
        return "invalid signature", 400

    order_id = request.form.get("platform_order_id")
    update_purchase_status(order_id, status="paid")

    # Koç eşle
    game = request.form.get("product_name")
    time = request.form.get("time")  # shopier formuna gömülmeli
    level = request.form.get("note")  # seviye burada olabilir

    coach = get_available_coach(game, time)
    zoom_link = create_zoom_link(game, time)  # test için sabit link

    notify_coaches(game, time, level, zoom_link)

    return "ok", 200

from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/googleaa1a9047867b85a7.html')
def google_verification():
    return send_from_directory('static', 'googleaa1a9047867b85a7.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

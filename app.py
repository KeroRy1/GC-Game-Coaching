import os
import json
from flask import Flask, render_template, request, redirect, url_for
import iyzipay

app = Flask(__name__)

# İyzico API ayarları (sandbox için)
options = {
    'api_key': os.environ.get('IYZICO_API_KEY', 'sandbox_api_key'),
    'secret_key': os.environ.get('IYZICO_SECRET_KEY', 'sandbox_secret_key'),
    'base_url': 'https://sandbox-api.iyzipay.com'
}

games = ["Valorant", "CS2", "LoL"]
packages = [
    {"name": "Basit", "price_tl": 400, "features": ["Canlı Ders"]},
    {"name": "Orta", "price_tl": 600, "features": ["Canlı Ders", "PDF Rehber"]},
    {"name": "Pro", "price_tl": 1000, "features": ["Canlı Ders", "PDF Rehber", "Özel Koçluk"]},
    {"name": "Oyun Ustası", "price_tl": 1500, "features": ["Canlı Ders", "PDF Rehber", "Özel Koçluk", "1v1 Analiz"]}
]

feedbacks = []

# Koç profilleri
coaches = [
    {"id": 1, "name": "Ahmet Yılmaz", "game": "Valorant", "level": "Pro"},
    {"id": 2, "name": "Elif Demir", "game": "LoL", "level": "Orta"},
    {"id": 3, "name": "Can Kaya", "game": "CS2", "level": "Oyun Ustası"}
]

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
        return render_template("error.html", message="Geçersiz seçim. Lütfen tekrar deneyiniz."), 400
    try:
        hour = int(time.split(":")[0])
        if hour < 8:
            return render_template("error.html", message="Saat 08:00'den önce ders seçilemez."), 400
    except:
        return render_template("error.html", message="Saat formatı geçersiz."), 400

    conversation_id = "conv_" + os.urandom(8).hex()

    request_data = {
        'locale': 'tr',
        'conversationId': conversation_id,
        'price': str(package["price_tl"]),
        'paidPrice': str(package["price_tl"]),
        'currency': 'TRY',
        'basketId': 'B12345',
        'paymentGroup': 'PRODUCT',
        'callbackUrl': request.url_root + 'payment-result',
        'buyer': {
            'id': 'BY789',
            'name': 'Müşteri',
            'surname': 'Soyadı',
            'email': 'email@example.com',
            'gsmNumber': '+905551112233',
            'identityNumber': '11111111111',
            'registrationAddress': 'İstanbul',
            'city': 'İstanbul',
            'country': 'Türkiye',
            'zipCode': '34000'
        },
        'shippingAddress': {
            'contactName': 'Müşteri Soyadı',
            'city': 'İstanbul',
            'country': 'Türkiye',
            'address': 'İstanbul, Türkiye'
        },
        'billingAddress': {
            'contactName': 'Müşteri Soyadı',
            'city': 'İstanbul',
            'country': 'Türkiye',
            'address': 'İstanbul, Türkiye'
        },
        'basketItems': [{
            'id': 'BI101',
            'name': f"{game} - {package['name']} ({time})",
            'category1': 'Ders',
            'itemType': 'VIRTUAL',
            'price': str(package["price_tl"])
        }]
    }

    checkout_form_initialize_request = iyzipay.CheckoutFormInitializeRequest()
    checkout_form_initialize_request.set_locale(request_data['locale'])
    checkout_form_initialize_request.set_conversation_id(request_data['conversationId'])
    checkout_form_initialize_request.set_price(request_data['price'])
    checkout_form_initialize_request.set_paid_price(request_data['paidPrice'])
    checkout_form_initialize_request.set_currency(request_data['currency'])
    checkout_form_initialize_request.set_basket_id(request_data['basketId'])
    checkout_form_initialize_request.set_payment_group(request_data['paymentGroup'])
    checkout_form_initialize_request.set_callback_url(request_data['callbackUrl'])
    checkout_form_initialize_request.set_buyer(request_data['buyer'])
    checkout_form_initialize_request.set_shipping_address(request_data['shippingAddress'])
    checkout_form_initialize_request.set_billing_address(request_data['billingAddress'])
    checkout_form_initialize_request.set_basket_items(request_data['basketItems'])

    try:
        raw_checkout_form = iyzipay.CheckoutForm().create(checkout_form_initialize_request, options)
        checkout_form = json.loads(raw_checkout_form.read().decode('utf-8'))

        if checkout_form['status'] == 'success':
            return redirect(checkout_form['paymentPageUrl'])
        else:
            return render_template("error.html", message="Ödeme başlatılamadı. Lütfen daha sonra tekrar deneyiniz."), 400

    except Exception as e:
        print("Hata:", e)
        return render_template("error.html", message="Bir hata oluştu. API anahtarı eksik veya bağlantı kurulamadı."), 500

@app.route("/payment-result")
def payment_result():
    token = request.args.get('token')
    if not token:
        return "Geçersiz istek", 400

    request_obj = iyzipay.CheckoutFormResultRequest()
    request_obj.set_token(token)
    result_raw = iyzipay.CheckoutForm().retrieve(request_obj, options)
    result = json.loads(result_raw.read().decode('utf-8'))

    if result['status'] == 'success':
        return render_template("success.html", details=result)
    else:
        return render_template("cancel.html", error=result.get('errorMessage', 'Ödeme başarısız'))

@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    comment = request.form.get("comment")
    if comment:
        feedbacks.append(comment)
    return redirect(url_for("index"))

@app.route("/coaches")
def coach_list():
    return render_template("coaches.html", coaches=coaches)

@app.route("/coach/<int:coach_id>")
def coach_detail(coach_id):
    coach = next((c for c in coaches if c["id"] == coach_id), None)
    if not coach:
        return render_template("error.html", message="Koç bulunamadı."), 404
    return render_template("coach_detail.html", coach=coach)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

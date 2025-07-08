import os
import json
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from twilio.rest import Client
import iyzipay

app = Flask(__name__)

# İyzico API ayarları
options = {
    'api_key': os.environ.get('IYZICO_API_KEY', 'sandbox_api_key'),
    'secret_key': os.environ.get('IYZICO_SECRET_KEY', 'sandbox_secret_key'),
    'base_url': 'https://sandbox-api.iyzipay.com'
}

# Twilio ayarları
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
    return "https://zoom.us/j/" + str(os.urandom(4).hex())

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

    zoom_link = create_zoom_link()
    notify_admins(game, pkg, time, zoom_link)
    return render_template("success.html", zoom_link=zoom_link)

@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    comment = request.form.get("comment")
    if comment:
        feedbacks.append(comment)
    return redirect(url_for("index"))

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
        zoom_link = create_zoom_link()
        return render_template("redirecting.html", zoom_link=zoom_link)
    else:
        return render_template("cancel.html", error=result.get('errorMessage', 'Odeme basarisiz'))

@app.route("/coaches")
def coach_list():
    coaches = [
        {"id": 1, "name": "Ahmet Yılmaz", "game": "Valorant"},
        {"id": 2, "name": "Elif Demir", "game": "LoL"},
        {"id": 3, "name": "Can Kaya", "game": "CS2"}
    ]
    return render_template("coaches.html", coaches=coaches)

@app.route("/coach/<int:coach_id>")
def coach_detail(coach_id):
    coach = next((c for c in coaches if c["id"] == coach_id), None)
    if not coach:
        return render_template("error.html", message="Koç bulunamadı."), 404
    return render_template("coach_detail.html", coach=coach)

@app.route('/googleaa1a9047867b85a7.html')
def google_verify():
    return send_from_directory('static', 'googleaa1a9047867b85a7.html')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

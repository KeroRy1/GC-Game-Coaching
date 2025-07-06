import os
from flask import Flask, render_template, request, redirect, url_for
import stripe

app = Flask(__name__)

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

games = ["Valorant", "CS2", "LoL"]
packages = [
    {"name": "Basit", "price_tl": 400, "features": ["Canlı Ders"]},
    {"name": "Orta", "price_tl": 600, "features": ["Canlı Ders", "PDF Rehber"]},
    {"name": "Pro", "price_tl": 1000, "features": ["Canlı Ders", "PDF Rehber", "Özel Koçluk"]},
    {"name": "Oyun Ustası", "price_tl": 1500, "features": ["Canlı Ders", "PDF Rehber", "Özel Koçluk", "1v1 Analiz"]}
]

@app.route("/")
def index():
    publishable_key = os.environ.get("STRIPE_PUBLISHABLE_KEY")
    return render_template("index.html", games=games, packages=packages, publishable_key=publishable_key)

@app.route("/checkout", methods=["POST"])
def checkout():
    game = request.form.get("game")
    pkg = request.form.get("package")
    time = request.form.get("time")

    package = next((p for p in packages if p["name"] == pkg), None)

    if not game or not package or not time or int(time[:2]) < 8:
        return "Geçersiz seçim.", 400

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "try",
                "product_data": {
                    "name": f"{game} - {package['name']} ({time})"
                },
                "unit_amount": package["price_tl"] * 100
            },
            "quantity": 1
        }],
        mode="payment",
        success_url=request.url_root + "waiting",
        cancel_url=request.url_root + "cancel"
    )
    return redirect(session.url, code=303)

@app.route("/waiting")
def waiting():
    zoom_link = "https://zoom.us/fake-meeting-link"
    return render_template("waiting.html", zoom_link=zoom_link)

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/cancel")
def cancel():
    return render_template("cancel.html")
    
feedbacks = []

@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    comment = request.form.get("comment")
    if comment:
        feedbacks.append(comment)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

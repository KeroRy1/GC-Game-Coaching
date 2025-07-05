import os
import logging
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import stripe
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

# Stripe API anahtarı
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

# Veritabanı ayarları
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODELLER
class Coach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    game = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    availability = db.Column(db.String(500), nullable=False)
    contact = db.Column(db.String(200), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(200), unique=True, nullable=False)
    game = db.Column(db.String(50), nullable=False)
    package = db.Column(db.String(50), nullable=False)
    time_slot = db.Column(db.String(50), nullable=False)
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'))
    coach = db.relationship('Coach')

# ZAMAN DİLİMLERİ
TIME_SLOTS = [
    "16:00-17:00", "17:00-18:00", "18:00-19:00",
    "19:00-20:00", "20:00-21:00", "21:00-22:00"
]

# OYUNLAR VE PAKETLER
games = ["Valorant", "CS2", "LoL"]
packages = [
    {"name": "Basic",    "price_usd": 10, "features": ["Live Session"]},
    {"name": "Standard", "price_usd": 25, "features": ["Live Session", "PDF Guide"]},
    {"name": "Pro",      "price_usd": 25, "features": ["Live Session", "PDF Guide", "Private Coaching"]}
]

# KOÇLARI VERİTABANINA EKLE (eğer yoksa)
def seed_coaches():
    if not Coach.query.first():
        sample_coaches = [
            Coach(name="Alex",   game="Valorant", level="Basic",    availability="18:00-19:00,20:00-21:00", contact="discord.gg/alex"),
            Coach(name="Blake",  game="CS2",      level="Basic",    availability="19:00-20:00,21:00-22:00", contact="discord.gg/blake"),
            Coach(name="Casey",  game="LoL",      level="Basic",    availability="18:00-19:00,21:00-22:00", contact="discord.gg/casey"),
            Coach(name="Dana",   game="Valorant", level="Standard", availability="17:00-18:00,19:00-20:00", contact="discord.gg/dana"),
            Coach(name="Eli",    game="CS2",      level="Standard", availability="18:00-19:00,20:00-21:00", contact="discord.gg/eli"),
            Coach(name="Finn",   game="LoL",      level="Standard", availability="17:00-18:00,21:00-22:00", contact="discord.gg/finn"),
            Coach(name="Grace",  game="Valorant", level="Pro",      availability="16:00-17:00,18:00-19:00", contact="discord.gg/grace"),
            Coach(name="Hayden", game="CS2",      level="Pro",      availability="17:00-18:00,20:00-21:00", contact="discord.gg/hayden"),
            Coach(name="Ivy",    game="LoL",      level="Pro",      availability="16:00-17:00,21:00-22:00", contact="discord.gg/ivy")
        ]
        db.session.bulk_save_objects(sample_coaches)
        db.session.commit()

# ANASAYFA
@app.route("/")
def index():
    return render_template("index.html", games=games, packages=packages, time_slots=TIME_SLOTS)

# CHECKOUT
@app.route("/checkout", methods=["POST"])
def checkout():
    game = request.form.get("game")
    pkg = request.form.get("package")
    time_slot = request.form.get("time_slot")

    package = next((p for p in packages if p["name"] == pkg), None)
    if not game or not package or time_slot not in TIME_SLOTS:
        return "Invalid selection.", 400

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": f"{game} – {pkg} Coaching Package"},
                "unit_amount": package["price_usd"] * 100
            },
            "quantity": 1
        }],
        mode="payment",
        success_url=request.url_root + "success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.url_root + "cancel"
    )

    order = Order(session_id=session.id, game=game, package=pkg, time_slot=time_slot)
    db.session.add(order)
    db.session.commit()

    return redirect(session.url, code=303)

# BAŞARILI ÖDEME
@app.route("/success")
def success():
    session_id = request.args.get("session_id")
    order = Order.query.filter_by(session_id=session_id).first_or_404()

    candidates = Coach.query.filter_by(game=order.game, level=order.package).all()
    available = [c for c in candidates if order.time_slot in c.availability.split(",")]

    return render_template("success.html", coach_list=available, time_slot=order.time_slot)

# İPTAL
@app.route("/cancel")
def cancel():
    return render_template("cancel.html")

# UYGULAMA BAŞLATILDIĞINDA DB OLUŞTUR VE KOÇLARI EKLE
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_coaches()
    app.run(host="0.0.0.0", debug=True)

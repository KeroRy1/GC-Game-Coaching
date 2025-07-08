import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))
admins = os.getenv("ADMIN_NUMBERS").split(",")

def notify_coaches(game, time, level, link):
    msg = f"🕹 Yeni Seans: {game}\nSeviye: {level}\nSaat: {time}\nZoom: {link}"
    for admin in admins:
        client.messages.create(
            body=msg,
            from_='whatsapp:' + os.getenv("TWILIO_WHATSAPP_NUMBER"),
            to='whatsapp:' + admin.strip()
        )

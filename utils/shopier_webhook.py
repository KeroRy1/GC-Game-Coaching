import hashlib
import hmac
import os

def verify_shopier_signature(form_data):
    signature = form_data.get("signature")
    secret = os.getenv("SHOPIER_SECRET")

    data_string = f"{form_data.get('platform_order_id')}{form_data.get('payment_id')}"
    calculated = hmac.new(secret.encode(), data_string.encode(), hashlib.sha256).hexdigest()

    return calculated == signature

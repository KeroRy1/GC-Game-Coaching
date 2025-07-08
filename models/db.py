# Yerine gerçek DB entegresi yapılmalı

sample_coaches = [
    {"name": "Ahmet", "game": "Valorant", "time": "15:00"},
    {"name": "Elif", "game": "LoL", "time": "16:00"}
]

purchases = {}

def save_purchase(game, level, time):
    pid = str(len(purchases) + 1)
    purchases[pid] = {"game": game, "level": level, "time": time, "status": "pending"}
    return pid

def update_purchase_status(pid, status):
    if pid in purchases:
        purchases[pid]["status"] = status

def get_available_coach(game, time):
    for coach in sample_coaches:
        if coach["game"] == game and coach["time"] == time:
            return coach
    return None

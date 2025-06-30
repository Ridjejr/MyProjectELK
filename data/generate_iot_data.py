import socket, json, time, random
from datetime import datetime

# Générateur de données IoT pour les résultats de la Premier League
def generate():
    return {
        "timestamp": datetime.now().isoformat(),
        "sensor_id": f"sensor_{random.randint(1, 20)}",
        "team_home": random.choice(["Arsenal", "Chelsea", "Liverpool"]),
        "team_away": random.choice(["Man City", "Tottenham", "Everton"]),
        "score_home": random.randint(0,5),
        "score_away": random.randint(0,5),
        "latitude": round(random.uniform(51.48, 51.60), 6),
        "longitude": round(random.uniform(-0.12, 0.10), 6),
        "stadium": random.choice([
        "Emirates", "Stamford Bridge", "Anfield", 
        "Etihad", "Tottenham Hotspur Stadium", "Goodison Park"
        ]),
        "weather": random.choice(["Ensoleillé", "Pluvieux", "Nuageux", "Venteux"]),
        "temperature": round(random.uniform(5, 25), 1),
        "humidity": random.randint(30, 90),
        "yellow_cards_home": random.randint(0, 5),
        "red_cards_home": random.randint(0, 2),
        "yellow_cards_away": random.randint(0, 5),
    }

# Connexion au serveur TCP
HOST, PORT = "localhost", 5045
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Envoi de données toutes les secondes
while True:
    message = json.dumps(generate()) + "\n"
    sock.sendall(message.encode())
    time.sleep(1)

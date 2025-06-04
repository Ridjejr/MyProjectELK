import csv
import random

pilotes = ["Verstappen", "Hamilton", "Leclerc"]

circuits = {
    "Jeddah": 50,
    "Monza": 53,
    "Barcelone": 66,
    "Monaco": 78
}

with open("f1_telemetry.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    # On ajoute la colonne pit_stop
    writer.writerow(["circuit", "tour", "pilote", "vitesse", "temp_moteur", "pit_stop"])
    
    for circuit, nb_tours in circuits.items():
        # Pour chaque pilote, on choisit aléatoirement 1 à 3 tours pour les pit stops
        pit_stops_pilotes = {}
        for pilote in pilotes:
            nb_pitstops = random.randint(1, 3)
            pit_stops_pilotes[pilote] = random.sample(range(2, nb_tours), nb_pitstops) # Jamais au 1er tour ni au dernier

        for tour in range(1, nb_tours + 1):
            for pilote in pilotes:
                vitesse = round(random.uniform(200, 340), 1)
                temp_moteur = round(random.uniform(90, 110), 1)
                # Vérifie si ce tour est un pit stop pour le pilote
                pit_stop = 1 if tour in pit_stops_pilotes[pilote] else 0
                writer.writerow([circuit, tour, pilote, vitesse, temp_moteur, pit_stop])

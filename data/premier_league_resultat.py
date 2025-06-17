import requests
import csv
from collections import defaultdict

# === CONFIGURATION ===
API_KEY = "f2f889adca4439e2dc419e436473cdbb"
BASE_URL = "https://v3.football.api-sports.io"
LEAGUE_ID = 39      # Premier League
SEASON = 2022       # Utilise 2023 car la saison 2024/2025 n'a pas commencé

headers = {
    "x-apisports-key": API_KEY
}

# Récupération des matchs
print(" Récupération des matchs de Premier League...")
res = requests.get(
    f"{BASE_URL}/fixtures",
    headers=headers,
    params={"league": LEAGUE_ID, "season": SEASON}
)

data = res.json()
fixtures = data["response"]

matches = []
for match in fixtures:
    info = match["fixture"]
    teams = match["teams"]
    goals = match["goals"]

    if goals["home"] is None or goals["away"] is None:
        continue  # match non joué

    matches.append([
        info["date"][:10],                          # format YYYY-MM-DD
        teams["home"]["name"],
        teams["away"]["name"],
        goals["home"],
        goals["away"]
    ])

#  Sauvegarde des résultats
with open("premier_league_resultat.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "team_home", "team_away", "score_home", "score_away"])
    writer.writerows(matches)

print(f" {len(matches)} matchs enregistrés dans premier_league_resultat.csv")

# Statistiques d’équipes 
goals_for = defaultdict(int)
goals_against = defaultdict(int)

for match in matches:
    _, home, away, score_home, score_away = match
    goals_for[home] += int(score_home)
    goals_against[home] += int(score_away)
    goals_for[away] += int(score_away)
    goals_against[away] += int(score_home)

with open("stats_equipes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["team", "goals_for", "goals_against"])
    for team in sorted(goals_for.keys()):
        writer.writerow([team, goals_for[team], goals_against[team]])

print(f" {len(goals_for)} équipes enregistrées dans stats_equipes.csv")

#  Classement général 
print(" Récupération du classement de la Premier League...")
res = requests.get(
    f"{BASE_URL}/standings",
    headers=headers,
    params={"league": LEAGUE_ID, "season": SEASON}
)

data = res.json()

try:
    standings = data["response"][0]["league"]["standings"][0]
except (IndexError, KeyError):
    print(" Erreur : Classement non disponible")
    standings = []

if standings:
    with open("classement.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "team", "played", "wins", "draws", "losses", "goals_for", "goals_against", "points"])
        for team in standings:
            writer.writerow([
                team["rank"],
                team["team"]["name"],
                team["all"]["played"],
                team["all"]["win"],
                team["all"]["draw"],
                team["all"]["lose"],
                team["all"]["goals"]["for"],
                team["all"]["goals"]["against"],
                team["points"]
            ])
    print(f" Classement exporté dans classement.csv")
else:
    print(" Aucun classement trouvé pour cette saison.")

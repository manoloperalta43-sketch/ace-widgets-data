import requests
from bs4 import BeautifulSoup
import json
from datetime import date

def get_atp_rankings():
    url = "https://en.wikipedia.org/wiki/ATP_rankings"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Buscar la tabla de rankings
    tables = soup.find_all("table", class_="wikitable")
    rankings = []
    previous = {}

    for table in tables:
        rows = table.find_all("tr")[1:]  # saltar header
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 3:
                continue

            rank = cols[0].get_text(strip=True)
            name = cols[1].get_text(strip=True)
            points = cols[2].get_text(strip=True).replace(",", "")

            if not rank.isdigit():
                continue

            rank = int(rank)
            if rank > 5:
                break

            # Movimiento (si existe columna)
            move = 0
            if len(cols) >= 4:
                move_text = cols[3].get_text(strip=True)
                try:
                    move = int(move_text.replace("+", ""))
                except:
                    move = 0

            if move > 0:
                movement = f"▲+{move}"
            elif move < 0:
                movement = f"▼{move}"
            else:
                movement = "–"

            rankings.append({
                "rank": rank,
                "name": name,
                "points": int(points) if points.isdigit() else 0,
                "movement": movement
            })

        if rankings:
            break

    return rankings

data = {
    "updated_at": str(date.today()),
    "rankings": get_atp_rankings()
}

with open("rankings.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("JSON generado:", data)

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import date

def clean_name(name):
    return re.sub(r'\(.*?\)', '', name).strip()

def get_atp_rankings():
    url = "https://en.wikipedia.org/wiki/ATP_rankings"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table", class_="wikitable")
    rankings = []

    # La segunda tabla es el ranking ATP oficial (52 semanas)
    table = tables[1]
    rows = table.find_all("tr")[1:]

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        rank = cols[0].get_text(strip=True)
        if not rank.isdigit():
            continue

        rank = int(rank)
        if rank > 5:
            break

        name = clean_name(cols[1].get_text(strip=True))
        points_text = cols[2].get_text(strip=True).replace(",", "").replace(".", "")
        points = int(points_text) if points_text.isdigit() else 0

        # Movimiento real de Wikipedia
        movement = "–"
        if len(cols) >= 4:
            move_text = cols[3].get_text(strip=True)
            match = re.search(r'(\d+)', move_text)
            if match:
                move = int(match.group(1))
                if "▲" in move_text or "▴" in move_text:
                    movement = f"▲+{move}"
                elif "▼" in move_text or "▾" in move_text:
                    movement = f"▼-{move}"
            elif "—" in move_text or "-" in move_text:
                movement = "–"

        rankings.append({
            "rank": rank,
            "name": name,
            "points": points,
            "movement": movement
        })

    return rankings

data = {
    "updated_at": str(date.today()),
    "rankings": get_atp_rankings()
}

with open("rankings.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("JSON generado:", data)

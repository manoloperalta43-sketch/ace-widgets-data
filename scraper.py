import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/ATP_rankings"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all("table", class_="wikitable")
print(f"Total tablas encontradas: {len(tables)}")

for i, table in enumerate(tables):
    rows = table.find_all("tr")
    print(f"\n--- Tabla {i} ({len(rows)} filas) ---")
    for row in rows[:3]:  # Solo primeras 3 filas
        cols = row.find_all(["th", "td"])
        print([c.get_text(strip=True) for c in cols])

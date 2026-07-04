import csv
import random
from datetime import datetime, timedelta

rows = []
start = datetime(2026, 7, 4, 10, 0, 0)

for i in range(60):
    timestamp = start + timedelta(seconds=i * 5)

    step = min(5, 1 + i // 12)

    rows.append({
        "timestamp": timestamp.isoformat(),
        "aktueller_schritt": step,
        "alarm": "true" if i > 45 else "false",
        "durchfluss": round(random.uniform(3.0, 4.8), 2),
        "k1_temperatur": round(62 + i * 0.25 + random.uniform(-0.4, 0.4), 1),
        "k2_fuellstand": min(100, 70 + i),
        "k2_temperatur": round(58 + i * 0.18 + random.uniform(-0.3, 0.3), 1),
        "k3_fuellstand": min(100, 35 + i),
        "k3_temperatur": round(54 + i * 0.15 + random.uniform(-0.3, 0.3), 1),
    })

with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("data.csv wurde erfolgreich aktualisiert.")

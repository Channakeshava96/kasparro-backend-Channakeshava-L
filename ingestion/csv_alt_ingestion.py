import csv
from pathlib import Path

CSV_ALT_PATH = Path("data/prices_alt.csv")

def read_alt_csv_data():
    rows = []

    with open(CSV_ALT_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    return rows

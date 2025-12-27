import csv
from pathlib import Path

CSV_PATH = Path("data/prices.csv")

def read_csv_data():
    rows = []

    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    return rows

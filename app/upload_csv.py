#upload_csv.py
from fastapi import UploadFile
from database import insert_index, insert_currency_pair, get_connection
import csv

async def process_uploaded_csv(file: UploadFile):
    contents = await file.read()
    decoded = contents.decode("utf-8").splitlines()
    reader = csv.DictReader(decoded)

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Indexes")
        cursor.execute("ALTER TABLE Indexes AUTO_INCREMENT = 1")
        cursor.execute("DELETE FROM CurrencyPairs")
        cursor.execute("ALTER TABLE CurrencyPairs AUTO_INCREMENT = 1")
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    for row in reader:
        if row["type"] == "Index":
            name = row.get("name")
            value = row.get("value")
            if name and value:
                insert_index(name, float(value))
        elif row["type"] == "CurrencyPair":
            base = row.get("baseCurrency")
            quote = row.get("quoteCurrency")
            rate = row.get("exchangeRate")
            if base and quote and rate:
                insert_currency_pair(base, quote, float(rate))

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MAX(id) FROM Indexes")
        max_index_id = cursor.fetchone()[0] or 0
        cursor.execute(f"ALTER TABLE Indexes AUTO_INCREMENT = {max_index_id + 1}")

        cursor.execute("SELECT MAX(id) FROM CurrencyPairs")
        max_pair_id = cursor.fetchone()[0] or 0
        cursor.execute(f"ALTER TABLE CurrencyPairs AUTO_INCREMENT = {max_pair_id + 1}")

        conn.commit()
    finally:
        cursor.close()
        conn.close()

import csv
import random

def generate_csv(filename="data/data.csv", rows=1000):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["type", "name", "value", "baseCurrency", "quoteCurrency", "exchangeRate"])
        for _ in range(rows):
            if random.choice([True, False]):
                name = f"Index_{random.randint(1, 100)}"
                value = round(random.uniform(1000, 10000), 2)
                writer.writerow(["Index", name, value, "", "", ""])
            else:
                base = random.choice(["USD", "EUR", "UAH", "GBP", "JPY"])
                quote = random.choice(["USD", "EUR", "UAH", "GBP", "JPY"])
                while quote == base:
                    quote = random.choice(["USD", "EUR", "UAH", "GBP", "JPY"])
                rate = round(random.uniform(0.1, 2.0), 4)
                writer.writerow(["CurrencyPair", "", "", base, quote, rate])

if __name__ == "__main__":
    generate_csv()

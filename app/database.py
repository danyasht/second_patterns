import mysql.connector
from mysql.connector import MySQLConnection

DB_CONFIG = {
    "user": "root",
    "password": "DANYA555777999shtog",
    "host": "localhost",
    "database": "finance_data",
}


def get_connection() -> MySQLConnection:
    return mysql.connector.connect(**DB_CONFIG)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Indexes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) UNIQUE,
                value DOUBLE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS CurrencyPairs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                baseCurrency VARCHAR(10),
                quoteCurrency VARCHAR(10),
                exchangeRate DOUBLE,
                UNIQUE (baseCurrency, quoteCurrency)
            );
        """)
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def insert_index(name: str, value: float):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Indexes (name, value) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE value = VALUES(value);
        """, (name, value))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def insert_currency_pair(base: str, quote: str, rate: float):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO CurrencyPairs (baseCurrency, quoteCurrency, exchangeRate) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE exchangeRate = VALUES(exchangeRate);
        """, (base, quote, rate))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

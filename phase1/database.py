# Standard Library
import time
import sqlite3

DB_NAME = "crypto_history.db"


class DBWriter:
    @staticmethod
    def get_last_ten_records():
        connection = DBWriter.get_connection()
        cursor = connection.cursor()
        results = cursor.execute(
            "SELECT crypto, usd_price, last_updated_at FROM CryptoPrice ORDER BY created_at DESC LIMIT ?",
            (10,),
        ).fetchall()
        connection.commit()
        connection.close()
        return results

    @staticmethod
    def insert_into_db(crypto_data):
        connection = DBWriter.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO CryptoPrice (crypto, usd_price, last_updated_at, created_at) VALUES (?, ?, ?, ?)",
            (
                crypto_data.crypto,
                crypto_data.usd,
                crypto_data.last_updated_at,
                time.time(),
            ),
        )
        connection.commit()
        connection.close()

    @staticmethod
    def db_init():
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS CryptoPrice
            (
                id INTEGER PRIMARY KEY,
                crypto TEXT NOT NULL,
                usd_price TEXT NOT NULL,
                last_updated_at INTEGER,
                created_at INTEGER
            )
            """
        )
        connection.commit()
        connection.close()

    @staticmethod
    def get_connection():
        connection = sqlite3.connect(DB_NAME)
        return connection


__all__ = ["DBWriter"]

"""
QAOS SQLite Persistence Backend
"""

import sqlite3

from .database import Database


class SQLiteStore(Database):

    def __init__(self, filename="qaos.db"):
        self.filename = filename

        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS storage (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """
        )

        connection.commit()
        connection.close()

    def save(self, key, value):

        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE
            INTO storage(key, value)
            VALUES (?, ?)
            """,
            (key, str(value))
        )

        connection.commit()
        connection.close()

    def load(self, key):

        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT value
            FROM storage
            WHERE key=?
            """,
            (key,)
        )

        row = cursor.fetchone()

        connection.close()

        if row:
            return row[0]

        return None

    def delete(self, key):

        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM storage
            WHERE key=?
            """,
            (key,)
        )

        connection.commit()
        connection.close()

    def all(self):

        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT key, value
            FROM storage
            """
        )

        rows = cursor.fetchall()

        connection.close()

        return {
            key: value
            for key, value in rows
        }
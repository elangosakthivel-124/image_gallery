import sqlite3
from datetime import datetime


class ImageDatabase:
    def __init__(self, db_name="gallery.db"):
        self.conn = sqlite3.connect(db_name)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL UNIQUE,
            added_at TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_image(self, file_name, file_path):
        try:
            self.conn.execute(
                "INSERT INTO images (file_name, file_path, added_at) VALUES (?, ?, ?)",
                (file_name, file_path, datetime.now().isoformat())
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass  # image already exists

    def get_all_images(self):
        cursor = self.conn.execute(
            "SELECT file_path FROM images ORDER BY added_at DESC"
        )
        return [row[0] for row in cursor.fetchall()]

    def close(self):
        self.conn.close()

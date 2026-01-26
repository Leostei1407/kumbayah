import sqlite3

class Database:
    def __init__(self, path='kumbayah.db'):
        self.path = path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()

    def create_tables(self):
        conn = self.connect()
        cur = conn.cursor()
        # Crear la tabla clients
        cur.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            phone TEXT UNIQUE
        )
        ''')
        # Tabla bookings normalizada que referencia a clients
        cur.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            date TEXT PRIMARY KEY,
            client_id INTEGER,
            amount REAL,
            payment_status TEXT,
            payment_method TEXT,
            reference TEXT,
            created_at TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(id)
        )
        ''')
        conn.commit()

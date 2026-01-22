import sqlite3
from datetime import datetime


class Database:
    def __init__(self, path='kumbayah.db'):
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        cur = self.conn.cursor()
        # Crear la tabla clients
        cur.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            phone TEXT
        )
        ''')
        # Tabla bookings normalizada que referencia a clients (sin columna 'blocked')
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
        self.conn.commit()

        # Migrar esquemas antiguos si existen
        # 1) Si la tabla bookings antigua contiene campos de cliente, migrarlos a clients + bookings
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bookings'")
        if cur.fetchone():
            cur.execute("PRAGMA table_info(bookings)")
            cols = [r['name'] for r in cur.fetchall()]
            if 'first_name' in cols or 'last_name' in cols or 'phone' in cols:
                cur.execute('ALTER TABLE bookings RENAME TO bookings_old')
                cur.execute('''
                CREATE TABLE IF NOT EXISTS bookings_new (
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
                cur.execute('SELECT * FROM bookings_old')
                rows = cur.fetchall()
                for row in rows:
                    phone = row['phone'] if 'phone' in row.keys() else None
                    first = row['first_name'] if 'first_name' in row.keys() else ''
                    last = row['last_name'] if 'last_name' in row.keys() else ''
                    client_id = None
                    if phone:
                        cur.execute('SELECT id FROM clients WHERE phone=?', (phone,))
                        r = cur.fetchone()
                        if r:
                            client_id = r['id']
                    if client_id is None:
                        cur.execute('INSERT INTO clients (first_name, last_name, phone) VALUES (?,?,?)', (first, last, phone))
                        client_id = cur.lastrowid
                    cur.execute('INSERT OR REPLACE INTO bookings_new (date, client_id, amount, payment_status, payment_method, reference, created_at) VALUES (?,?,?,?,?,?,?)',
                                (row['date'], client_id, row.get('amount', 0.0), row.get('payment_status',''), row.get('payment_method',''), row.get('reference',''), row.get('created_at', datetime.utcnow().isoformat())))
                cur.execute('DROP TABLE IF EXISTS bookings_old')
                cur.execute('ALTER TABLE bookings_new RENAME TO bookings')
                self.conn.commit()

        # 2) Si existía la tabla availability, migrar fechas bloqueadas a bookings (client_id NULL)
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='availability'")
        if cur.fetchone():
            cur.execute('SELECT date, available FROM availability')
            rows = cur.fetchall()
            for r in rows:
                if r['available'] == 0:
                    # marcar como no disponible: almacenar fila de booking sin cliente
                    cur.execute('INSERT OR REPLACE INTO bookings (date, client_id, amount, payment_status, payment_method, reference, created_at) VALUES (?,?,?,?,?,?,?)',
                                (r['date'], None, 0.0, '', '', '', datetime.utcnow().isoformat()))
            cur.execute('DROP TABLE IF EXISTS availability')
            self.conn.commit()

    def add_booking(self, data: dict):
        cur = self.conn.cursor()
        # Asegurar que el cliente exista o crearlo
        client_id = data.get('client_id')
        if client_id is None:
            phone = data.get('phone','')
            first = data.get('first_name','')
            last = data.get('last_name','')
            client_id = None
            if phone:
                cur.execute('SELECT id FROM clients WHERE phone=?', (phone,))
                row = cur.fetchone()
                if row:
                    client_id = row['id']
            if client_id is None:
                cur.execute('INSERT INTO clients (first_name, last_name, phone) VALUES (?,?,?)', (first, last, phone))
                client_id = cur.lastrowid

        cur.execute('REPLACE INTO bookings (date, client_id, amount, payment_status, payment_method, reference, created_at) VALUES (?,?,?,?,?,?,?)',
                (data['date'], client_id, data.get('amount', 0.0), data.get('payment_status',''), data.get('payment_method',''), data.get('reference',''), datetime.utcnow().isoformat()))
        self.conn.commit()

    def get_booking(self, date_str):
        cur = self.conn.cursor()
        cur.execute('''
        SELECT b.date, b.amount, b.payment_status, b.payment_method, b.reference, b.created_at,
               c.id as client_id, c.first_name, c.last_name, c.phone
        FROM bookings b
        LEFT JOIN clients c ON b.client_id = c.id
        WHERE b.date = ?
        ''', (date_str,))
        row = cur.fetchone()
        if not row:
            return None
        d = dict(row)
        # Si la reserva existe pero no tiene cliente (día no disponible), tratar como sin reserva para mostrar al usuario
        if d.get('client_id') is None:
            return None
        return d

    def delete_booking(self, date_str):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM bookings WHERE date=?', (date_str,))
        self.conn.commit()

    def is_available(self, date_str):
        cur = self.conn.cursor()
        cur.execute('SELECT client_id FROM bookings WHERE date=?', (date_str,))
        row = cur.fetchone()
        # disponible si no hay un registro de booking para esa fecha
        return row is None

    def set_availability(self, date_str, available:int):
        cur = self.conn.cursor()
        if available:
            # eliminar booking sin cliente si existe
            cur.execute('SELECT client_id FROM bookings WHERE date=?', (date_str,))
            r = cur.fetchone()
            if r and r['client_id'] is None:
                cur.execute('DELETE FROM bookings WHERE date=?', (date_str,))
        else:
            # crear una entrada de booking sin cliente para marcar como no disponible
            cur.execute('INSERT OR REPLACE INTO bookings (date, client_id, amount, payment_status, payment_method, reference, created_at) VALUES (?,?,?,?,?,?,?)',
                        (date_str, None, 0.0, '', '', '', datetime.utcnow().isoformat()))
        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    db = Database('test_kumbayah.db')
    db.add_booking({'date':'2026-01-01','first_name':'Test','last_name':'User','phone':'123456','amount':100.0,'payment_status':'Completo','payment_method':'Efectivo','reference':''})
    print(db.get_booking('2026-01-01'))
    db.delete_booking('2026-01-01')
    db.close()

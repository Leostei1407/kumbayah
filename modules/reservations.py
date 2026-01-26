from datetime import datetime

class Reservations:
    def __init__(self, db_conn):
        self.conn = db_conn

    def add_booking(self, data: dict, client_id: int):
        cur = self.conn.cursor()
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
        return row is None

    def set_availability(self, date_str, available:int):
        cur = self.conn.cursor()
        if available:
            cur.execute('DELETE FROM bookings WHERE date=? AND client_id IS NULL', (date_str,))
        else:
            cur.execute('INSERT OR IGNORE INTO bookings (date, client_id, created_at) VALUES (?,?,?)',
                        (date_str, None, datetime.utcnow().isoformat()))
        self.conn.commit()

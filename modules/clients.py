
class Clients:
    def __init__(self, db_conn):
        self.conn = db_conn

    def add_or_get_client(self, first_name, last_name, phone):
        cur = self.conn.cursor()
        if not phone:
            cur.execute('INSERT INTO clients (first_name, last_name, phone) VALUES (?,?,?)', (first_name, last_name, None))
            return cur.lastrowid

        cur.execute('SELECT id FROM clients WHERE phone=?', (phone,))
        row = cur.fetchone()
        if row:
            # Opcional: Actualizar nombre y apellido si han cambiado
            cur.execute('UPDATE clients SET first_name=?, last_name=? WHERE id=?', (first_name, last_name, row['id']))
            self.conn.commit()
            return row['id']
        else:
            cur.execute('INSERT INTO clients (first_name, last_name, phone) VALUES (?,?,?)', (first_name, last_name, phone))
            self.conn.commit()
            return cur.lastrowid

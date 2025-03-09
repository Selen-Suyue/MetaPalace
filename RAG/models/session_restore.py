import sqlite3 as sql

SQL_DIR = './RAG/db/sqlite'
DB_NAME = 'session.db'

session_db = sql.connect(f'{SQL_DIR}\\{DB_NAME}')

def create_table():
    session_db.cursor().execute('''
        CREATE TABLE IF NOT EXISTS session(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            message STRING,
            type STRING
        )
    ''')
    session_db.commit()

class SessionRestore:
    def __init__(self):
        create_table()
        self.session_db = sql.connect(f'{SQL_DIR}\\{DB_NAME}')
        self.cursor = self.session_db.cursor()

    def insert(self, session_id: int, message: str, type: str):
        self.cursor.execute('''
            INSERT INTO session(session_id, message, type)
            VALUES(?, ?, ?)
        ''', (session_id, message, type))
        self.session_db.commit()

    def select(self, session_id: int):
        self.cursor.execute('''
            SELECT message, type
            FROM session
            WHERE session_id = ?
        ''', (session_id,))
        return self.cursor.fetchall()
    
if __name__ == '__main__':
    session_restore = SessionRestore()
    session_restore.insert(1, '你好', 'user')
    print(session_restore.select(1))
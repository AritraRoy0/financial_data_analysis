import sqlite3

DB_NAME = "finance.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_transactions(df):
    conn = sqlite3.connect(DB_NAME)
    df.to_sql('transactions', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()

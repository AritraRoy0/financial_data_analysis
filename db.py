import sqlite3

DB_NAME = "finance.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Drop the table if it exists to reset the database
    cursor.execute("DROP TABLE IF EXISTS transactions")
    
    # Create the table fresh
    cursor.execute("""
        CREATE TABLE transactions (
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
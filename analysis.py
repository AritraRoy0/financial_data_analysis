import sqlite3
import pandas as pd

DB_NAME = "finance.db"

def get_spending_by_category():
    conn = sqlite3.connect(DB_NAME)
    
    try:
        df = pd.read_sql("SELECT * FROM transactions", conn)
    except Exception as e:
        print(f"Error reading from database: {e}")
        conn.close()
        return
    
    conn.close()

    if df.empty:
        print("No transactions found in database!")
        return

    # Convert amount to numeric just in case
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df.dropna(subset=['amount'])

    if df.empty:
        print("No valid amounts found!")
        return

    # Group by category and sum amounts
    summary = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    total = summary.sum()

    print("\n" + "="*40)
    print("SPENDING BY CATEGORY")
    print("="*40)
    
    for category, amount in summary.items():
        percentage = (amount / total) * 100 if total != 0 else 0
        print(f"{category:<20} ${amount:>8.2f} ({percentage:5.1f}%)")
    
    print("-" * 40)
    print(f"{'TOTAL':<20} ${total:>8.2f} (100.0%)")
    print("=" * 40)

if __name__ == "__main__":
    get_spending_by_category()
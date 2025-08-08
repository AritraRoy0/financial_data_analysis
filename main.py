import os
from CSV_importer import load_transactions
from db import init_db, insert_transactions
from analysis import get_spending_by_category

if __name__ == "__main__":
    print("=== Finance Tracker ===")
    
    # Check if CSV exists
    csv_file = "transactions.csv"
    if not os.path.exists(csv_file):
        print(f"ERROR: {csv_file} not found!")
        print(f"Current directory: {os.getcwd()}")
        print(f"Files available: {[f for f in os.listdir('.') if f.endswith('.csv')]}")
        exit(1)
    
    # Initialize database
    init_db()
    print("Database initialized.")
    
    # Load and debug CSV
    print(f"\nLoading {csv_file}...")
    df = load_transactions(csv_file)
    
    if df.empty:
        print("No transactions loaded. Check the debug output above.")
        exit(1)
    
    print(f"\nLoaded {len(df)} transactions successfully!")
    
    # Insert into database
    insert_transactions(df)
    print("Transactions saved to database.")
    
    # Show summary
    get_spending_by_category()
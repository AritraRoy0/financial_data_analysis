# Finance Tracker CLI

A Python command-line tool that parses a bank CSV export, categorizes debit transactions, stores them in a local SQLite database, and prints a clean **“Spending by Category”** summary.

---

## Features

- Load transactions from a bank CSV file (`transactions.csv`)
- Filter only **debit** transactions
- Automatically categorize transactions (Food & Dining, Groceries, Transportation, ATM Withdrawal, Fees, etc.)
- Store cleaned transactions in a local SQLite database (`finance.db`)
- Display a formatted spending summary with category totals and percentages

---

## How It Works

The app follows a simple pipeline:

### 1. CSV Import (`CSV_importer.py`)
- Reads `transactions.csv`
- Filters for debit transactions
- Normalizes amounts (e.g., converts negative values into positive spending amounts)
- Uses basic keyword matching on the **Description** field to assign each transaction to a category

Example categorization rules (simplified):
- Contains `UBER`, `MBTA` → **Transportation**
- Contains `DOORDASH`, `CHIPOTLE`, `DUNKIN`, `MCDONALD`, `PIZZA` → **Food & Dining**
- Contains `TARGET`, `CVS`, `PHARMACY`, `H MART` → **Groceries**
- Contains `ATM` and `WITHDRAWAL`/`DEBIT` → **ATM Withdrawal**
- Contains `APPLE CASH` → **Money Transfer**
- Contains `FEE` → **Bank Fees**
- Everything else → **Other**

These rules are implemented and can be customized inside `CSV_importer.py`.

### 2. Database Storage (`db.py`)
- Creates (or recreates) a SQLite database (`finance.db`)
- Drops and recreates a `transactions` table each run (clean slate)
- Inserts all cleaned and categorized transactions into the `transactions` table

### 3. Spending Analysis (`analysis.py`)
- Connects to `finance.db`
- Reads all rows from the `transactions` table
- Aggregates the total spending for each category
- Calculates category percentages of total spending
- Prints a nicely formatted **“SPENDING BY CATEGORY”** summary to the terminal

---

## Requirements

- **Python** 3.9+ (earlier versions may work but are not guaranteed)
- **pip** for dependency management

Python libraries used:
- `pandas` (third-party)
- `sqlite3` (standard library)
- `os` (standard library)

---

## Installation

1. Clone the Repository  
   git clone https://github.com/<your-username>/<repo-name>.git  
   cd <repo-name>

2. Create a Virtual Environment (optional)  
   python -m venv venv

   Windows: venv\Scripts\activate  
   macOS / Linux: source venv/bin/activate

3. Install Dependencies  
   pip install pandas

---

## CSV Format

The project expects a CSV file named:

transactions.csv

---

## Usage

Export your bank transactions as a CSV file and save it as:

transactions.csv

in the same directory as main.py.


in the same directory as main.py.

Run the main script:

python main.py

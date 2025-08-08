import pandas as pd
import os

def load_transactions(file_path):
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"ERROR: File '{file_path}' not found!")
        return pd.DataFrame(columns=['amount', 'category'])
    
    # Load CSV - let's check the structure first
    df = pd.read_csv(file_path)
    print(f"Loaded CSV with {len(df)} rows")
    print(f"Columns: {list(df.columns)}")
    
    if df.empty:
        print("CSV file is empty!")
        return pd.DataFrame(columns=['amount', 'category'])
    
    # The issue is your CSV structure - let's reload it properly
    # Looking at your original data, it should be:
    # Details,Posting Date,Description,Amount,Type,Balance,Check or Slip #
    
    valid_rows = []
    
    for idx, row in df.iterrows():
        # The transaction type seems to be in the index/name, not the Details column
        # Let's check both the index name and the first column
        transaction_type = row.name if hasattr(row, 'name') else None
        
        # Also check if 'DEBIT' is in the first actual column value
        first_col_value = str(row.iloc[0]) if len(row) > 0 else ""
        
        print(f"Row {idx}: Index/Name = '{transaction_type}', First column = '{first_col_value}'")
        
        # Only process if this is a DEBIT transaction
        if transaction_type != 'DEBIT' and 'DEBIT' not in first_col_value:
            continue
            
        print(f"Processing DEBIT row {idx}")
        
        # The amount appears to be in the Description column based on your debug output
        try:
            # Try to get amount from Description column (which seems to contain the dollar amounts)
            amount_str = str(row['Description'])
            amount = float(amount_str)
            amount = int(abs(amount))  # Convert to positive integer
            
            print(f"Amount: {amount}")
            
            # Get description - this might be in a different column
            # Let's try the Posting Date column which might contain the actual description
            description = str(row['Posting Date'])
            
            print(f"Description: {description[:50]}...")
            
            # Categorize based on description content
            if 'UBER' in description:
                category = 'Transportation'
            elif 'DOORDASH' in description or 'DD *DOORDASH' in description:
                category = 'Food Delivery'
            elif any(x in description for x in ['MCDONALD', 'CHIPOTLE', 'DUNKIN']):
                category = 'Fast Food'
            elif any(x in description for x in ['CVS', 'PHARMACY']):
                category = 'Pharmacy'
            elif 'ATM' in description and ('WITHDRAWAL' in description or 'DEBIT' in description):
                category = 'ATM Withdrawal'
            elif any(x in description for x in ['H MART', 'STAR OSCO', 'TARGET']):
                category = 'Groceries'
            elif any(x in description for x in ['HALSTED', 'TD BANK']) and 'PAYMENT' in description:
                category = 'Loan Payment'
            elif 'SMOKE SHOP' in description:
                category = 'Tobacco'
            elif any(x in description for x in ['RAMEN', 'SAPPORO', 'CURRY', 'PIZZA', 'BURGER', 'IHOP', 'JAMAICA']):
                category = 'Restaurant'
            elif 'APPLE CASH' in description:
                category = 'Money Transfer'
            elif 'MBTA' in description:
                category = 'Transportation'
            elif 'FEE' in description:
                category = 'Bank Fees'
            elif 'PARCHMENT' in description:
                category = 'Education/Documents'
            elif 'TASTY BURGER' in description:
                category = 'Fast Food'
            elif '7-ELEVEN' in description:
                category = 'Convenience Store'
            elif 'SHANGHAI FRESH' in description:
                category = 'Restaurant'
            else:
                category = 'Other'
            
            valid_rows.append({
                'amount': amount,
                'category': category
            })
            
        except (ValueError, TypeError) as e:
            print(f"Could not process row {idx}: {e}")
            continue
    
    # Create DataFrame
    result_df = pd.DataFrame(valid_rows)
    
    print(f"Extracted {len(result_df)} DEBIT transactions")
    if not result_df.empty:
        print("Categories found:", sorted(result_df['category'].unique().tolist()))
        print(f"Amount range: ${result_df['amount'].min()} to ${result_df['amount'].max()}")
        print(f"Total spending: ${result_df['amount'].sum()}")
    
    return result_df
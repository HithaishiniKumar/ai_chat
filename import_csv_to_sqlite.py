import pandas as pd
import sqlite3
import os

# Set your paths here
csv_files = {
    "total_sales": r"C:\Users\Hithaishini\Downloads\Product-Level Total Sales and Metrics (mapped) - Product-Level Total Sales and Metrics (mapped).csv",
    "ad_sales": r"C:\Users\Hithaishini\Downloads\Product-Level Ad Sales and Metrics (mapped) - Product-Level Ad Sales and Metrics (mapped).csv",
    "eligibility": r"C:\Users\Hithaishini\Downloads\Product-Level Eligibility Table (mapped) - Product-Level Eligibility Table (mapped).csv"
}

# Create SQLite DB file
conn = sqlite3.connect("ecommerce_data.db")

# Load each CSV into a separate table
for table_name, csv_path in csv_files.items():
    if os.path.exists(csv_path):
        print(f"Importing {table_name} from {csv_path}...")
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"✅ Table '{table_name}' created.")
    else:
        print(f"❌ File not found: {csv_path}")

conn.close()
print("🎉 All done! SQLite DB created: ecommerce_data.db")

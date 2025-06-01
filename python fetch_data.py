import sqlite3
import pandas as pd

# Connect to your database
conn = sqlite3.connect("sales_data.db")

# Example: Top 10 countries by revenue
query1 = "SELECT * FROM country_sales_view ORDER BY total_revenue DESC LIMIT 10;"
df_country = pd.read_sql(query1, conn)
print("\nTop 10 Countries by Revenue:")
print(df_country)

# Example: Top customers
query3 = "SELECT * FROM customer_summary_view ORDER BY total_spent DESC LIMIT 5;"
df_customers = pd.read_sql(query3, conn)
print("\nTop 5 Customers by Spending:")
print(df_customers)

conn.close()

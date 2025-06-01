import pandas as pd
import sqlite3

# Load cleaned CSV
df = pd.read_csv("cleaned_sales_data.csv")

# Connect to SQLite DB
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Save the dataframe to a table
df.to_sql("sales", conn, if_exists="replace", index=False)

# Create supporting table for JOINs
cursor.executescript("""
CREATE TABLE IF NOT EXISTS products AS
SELECT DISTINCT ProductNo, ProductName
FROM sales;
""")

# Create views, indexes, and run analysis queries
cursor.executescript("""
CREATE VIEW IF NOT EXISTS country_sales_view AS
SELECT Country, SUM(Quantity * Price) AS total_revenue, COUNT(*) AS total_orders
FROM sales
GROUP BY Country;

CREATE VIEW IF NOT EXISTS top_products_view AS
SELECT ProductName, SUM(Quantity) AS total_units_sold, SUM(Quantity * Price) AS total_revenue
FROM sales
GROUP BY ProductName;

CREATE VIEW IF NOT EXISTS customer_summary_view AS
SELECT CustomerNo, COUNT(*) AS num_orders, SUM(Quantity * Price) AS total_spent
FROM sales
GROUP BY CustomerNo;

CREATE INDEX IF NOT EXISTS idx_sales_country ON sales(Country);
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(Date);
CREATE INDEX IF NOT EXISTS idx_sales_customer ON sales(CustomerNo);
CREATE INDEX IF NOT EXISTS idx_sales_product ON sales(ProductNo);
""")

conn.commit()
conn.close()

print("SQL views and indexes created successfully in SQLite.")


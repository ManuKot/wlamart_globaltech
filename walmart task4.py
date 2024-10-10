import pandas as pd
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('walmart_data.db')
cursor = conn.cursor()

# Create tables (if they don't already exist)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    manufacturer TEXT,
    weight REAL,
    flavor TEXT,
    health_condition TEXT,
    material TEXT,
    durability INTEGER,
    color TEXT,
    size TEXT,
    care_instructions TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Shipments (
    id INTEGER PRIMARY KEY,
    shipping_identifier TEXT,
    origin TEXT,
    destination TEXT,
    date TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Transaction (
    id INTEGER PRIMARY KEY,
    customer_name TEXT,
    customer_email TEXT,
    date TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Transaction_Products (
    transaction_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (transaction_id) REFERENCES Transaction(id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);
''')

# Load data from the spreadsheets
# Adjust the file paths as necessary
spreadsheet_0 = pd.read_excel('path_to_spreadsheet_0.xlsx')
spreadsheet_1 = pd.read_excel('path_to_spreadsheet_1.xlsx')
spreadsheet_2 = pd.read_excel('path_to_spreadsheet_2.xlsx')

# Insert data from spreadsheet 0 directly into Products
for index, row in spreadsheet_0.iterrows():
    cursor.execute('''
    INSERT INTO Products (name, manufacturer, weight, flavor, health_condition)
    VALUES (?, ?, ?, ?, ?)
    ''', (row['name'], row['manufacturer'], row['weight'], row['flavor'], row['target_health_condition']))

# Prepare a mapping of shipping identifiers to origin/destination
shipping_info = {}
for index, row in spreadsheet_2.iterrows():
    shipping_info[row['shipping_identifier']] = (row['origin'], row['destination'])

# Process spreadsheet 1 and insert data into Shipments and Products
for index, row in spreadsheet_1.iterrows():
    shipping_id = row['shipping_identifier']
    product_name = row['product_name']
    quantity = row['quantity']

    # Insert or get the product id
    cursor.execute('SELECT id FROM Products WHERE name = ?', (product_name,))
    product = cursor.fetchone()
    
    if product is None:
        print(f"Product {product_name} not found.")
        continue

    product_id = product[0]

    # Insert the shipment data
    if shipping_id in shipping_info:
        origin, destination = shipping_info[shipping_id]
        cursor.execute('''
        INSERT INTO Shipments (shipping_identifier, origin, destination, date)
        VALUES (?, ?, ?, ?)
        ''', (shipping_id, origin, destination, row['date']))

        # Insert into Transaction_Products
        cursor.execute('''
        INSERT INTO Transaction_Products (transaction_id, product_id, quantity)
        VALUES (?, ?, ?)
        ''', (row['transaction_id'], product_id, quantity))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data insertion completed successfully.")

import sqlite3
import pandas as pd
from datetime import datetime

# Path to CSV file
csv_file = 'on_call_pharmacies.csv'

# Connect to SQLite database
conn = sqlite3.connect('pharmacies.db')
cursor = conn.cursor()

# Drop the existing table if it exists
cursor.execute('DROP TABLE IF EXISTS pharmacies')

# Create table for pharmacies with the correct columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pharmacies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Quartier TEXT NOT NULL,
        Name TEXT NOT NULL,
        Address TEXT NOT NULL,
        Phone TEXT,
        City TEXT NOT NULL,
        Garde_Status TEXT NOT NULL,
        Date TEXT NOT NULL
    )
''')

# Load the CSV file into a DataFrame
df = pd.read_csv(csv_file)
current_date = datetime.now().strftime('%m-%d-%Y')

# Insert data from DataFrame into the SQLite database, skipping rows with missing Name
for _, row in df.iterrows():
    # Check if Name is missing
    if pd.isna(row['Name']):
        continue  # Skip this row if Name is missing

    cursor.execute('''
        INSERT INTO pharmacies (Quartier, Name, Address, Phone, City, Garde_Status, DATE)
        VALUES (?,?, ?, ?, ?, ?, ?)
    ''', (row['District'],row['Name'], row['Address'], row['Phone'], row['City'], row['Garde_Status'], current_date))

# Commit and close the database connection
conn.commit()
conn.close()

print("Database populated with data from CSV file!")

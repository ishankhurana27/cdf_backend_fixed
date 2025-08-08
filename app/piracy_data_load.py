import pandas as pd
import psycopg2

# Step 1: Load the CSV
df = pd.read_csv("C:/Users/ishan/Downloads/pirate_attacks.csv")

# Step 2: Combine date (time is 'NA' everywhere, so skip it)
df['attack_datetime'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

# Step 3: Drop rows with invalid datetime
df = df.dropna(subset=['attack_datetime'])

# Step 4: Replace 'NA' strings with None to handle NULL values
df = df.replace("NA", None)

# Step 5: Select & reorder columns to match your PostgreSQL table
df = df[[  
    'attack_datetime', 'longitude', 'latitude', 'attack_type', 'location_description',
    'nearest_country', 'eez_country', 'shore_distance', 'shore_longitude',
    'shore_latitude', 'attack_description', 'vessel_name', 'vessel_type',
    'vessel_status', 'data_source'
]]

# Step 6: Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="ship",  # <-- change this
    user="postgres",           # <-- change this
    password="ishan2702"        # <-- change this
)
cursor = conn.cursor()

# Step 7: Insert each row into the table
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO pirate_attacks (
            attack_datetime, longitude, latitude, attack_type, location_description,
            nearest_country, eez_country, shore_distance, shore_longitude,
            shore_latitude, attack_description, vessel_name, vessel_type,
            vessel_status, data_source
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

# Step 8: Commit and close
conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully.")

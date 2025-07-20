import sqlite3
import pandas as pd
from scipy.stats import pearsonr
import json

# Connect to SQLite and import the data
conn = sqlite3.connect("retail.db")
cursor = conn.cursor()

# Read and execute SQL file
with open("retail_data.sql", "r") as f:
    sql_script = f.read()
cursor.executescript(sql_script)

# Load data into DataFrame
df = pd.read_sql_query("SELECT * FROM retail_data", conn)

# Calculate Pearson correlations
correlations = {}
pairs = [
    ("Promo_Spend", "Footfall"),
    ("Promo_Spend", "Returns"),
    ("Footfall", "Returns")
]

for col1, col2 in pairs:
    corr, _ = pearsonr(df[col1], df[col2])
    correlations[f"{col1}-{col2}"] = corr

# Find the strongest correlation by absolute value
strongest_pair = max(correlations.items(), key=lambda x: abs(x[1]))

# Prepare result
result = {
    "pair": strongest_pair[0],
    "correlation": round(strongest_pair[1], 4)
}

# Write to JSON
with open("result.json", "w") as f:
    json.dump(result, f, indent=2)

print("✅ Result saved to result.json:", result)

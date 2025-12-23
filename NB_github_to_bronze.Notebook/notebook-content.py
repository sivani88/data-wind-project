# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "6267907f-fdb3-4ba4-90c0-7288faee2b34",
# META       "default_lakehouse_name": "wind_bronze",
# META       "default_lakehouse_workspace_id": "00e69122-80e7-4974-8e82-5e52582fc33c",
# META       "known_lakehouses": [
# META         {
# META           "id": "6267907f-fdb3-4ba4-90c0-7288faee2b34"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

import requests
import os

# Lister les fichiers GitHub
api_url = "https://api.github.com/repos/mikailaltundas/datasets-for-training/contents/wind-power-dataset"
response = requests.get(api_url)
files_info = response.json()
csv_files = [f["name"] for f in files_info if f["name"].endswith(".csv")]

# Télécharger
base_url = "https://raw.githubusercontent.com/mikailaltundas/datasets-for-training/main/wind-power-dataset/"
os.makedirs("/lakehouse/default/Files/raw_data", exist_ok=True)

for file_name in csv_files:
    response = requests.get(base_url + file_name)
    with open(f"/lakehouse/default/Files/raw_data/{file_name}", "wb") as f:
        f.write(response.content)
    print(f"✓ {file_name}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.sql("DROP TABLE IF EXISTS wind_power")
# Charger tous les CSV
df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("Files/raw_data/")

# Sauvegarder avec dbo comme le prof
bronze_path = "abfss://repo_wind@onelake.dfs.fabric.microsoft.com/wind_bronze.Lakehouse/Tables/dbo/wind_table"
df.write.format("delta").mode("overwrite").save(bronze_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

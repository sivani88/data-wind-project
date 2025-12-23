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
import pandas as pd
from datetime import timedelta


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#base url for github raw CSV files
base_url = "https://raw.githubusercontent.com/mikailaltundas/datasets-for-training/main/wind-power-dataset/"

#path to the wind_power table in the Bronze lakhouse
bronze_table_path = "abfss://repo_wind@onelake.dfs.fabric.microsoft.com/wind_bronze.Lakehouse/Tables/dbo/wind_table"


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_spark = spark.read.format("delta").load(bronze_table_path)
df_pandas = df_spark.toPandas()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Find the most recent date
most_recent_date = pd.to_datetime(df_pandas['date'], format='%Y%m%d').max()
end_date = pd.Timestamp('2024-08-03')

# Loop through each missing day
current_date = most_recent_date + timedelta(days=1)

while current_date <= end_date:
    next_date = current_date.strftime('%Y%m%d')
    
    try:
        # Download and load new data in a Pandas DataFrame
        file_url = f"{base_url}{next_date}_wind_power_data.csv"
        df_pandas_new = pd.read_csv(file_url)
        df_pandas_new['date'] = pd.to_datetime(df_pandas_new['date'])
        
        # Convert to Spark DataFrame and append in wind_power table
        df_spark_new = spark.createDataFrame(df_pandas_new, schema=df_spark.schema)
        df_spark_new.write.format("delta").mode("append").save(bronze_table_path)
        print(f"✓ {next_date}")
    except:
        print(f"✗ {next_date} - fichier non trouvé")
    
    current_date += timedelta(days=1)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Reload data
df_spark = spark.read.format("delta").load(bronze_table_path)
df_pandas = df_spark.toPandas()



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

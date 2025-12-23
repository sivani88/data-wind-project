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
# META         },
# META         {
# META           "id": "69255059-660d-42ba-814d-5651d7c62dab"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Create a temporary view of the wind_power table
# MAGIC CREATE OR REPLACE TEMPORARY VIEW bronze_wind_power AS
# MAGIC SELECT *
# MAGIC FROM repo_wind.wind_bronze.dbo.wind_power;  

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * FROM bronze_wind_power


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Clean and enrich data
# MAGIC CREATE OR REPLACE TEMPORARY VIEW transformed_wind_power AS
# MAGIC SELECT
# MAGIC     production_id,
# MAGIC     date,
# MAGIC     turbine_name,
# MAGIC     capacity,
# MAGIC     location_name,
# MAGIC     latitude,
# MAGIC     longitude,
# MAGIC     region,
# MAGIC     status,
# MAGIC     responsible_department,
# MAGIC     wind_direction,
# MAGIC     ROUND(wind_speed, 2) AS wind_speed,
# MAGIC     ROUND(energy_produced, 2) AS energy_produced,
# MAGIC     DAY(date) AS day,
# MAGIC     MONTH(date) AS month,
# MAGIC     QUARTER(date) AS quarter,
# MAGIC     YEAR(date) AS year,
# MAGIC     REGEXP_REPLACE(time, '-', ':') AS time,
# MAGIC     CAST(SUBSTRING(time, 1, 2) AS INT) AS hour_of_day,
# MAGIC     CAST(SUBSTRING(time, 4, 2) AS INT) AS minute_of_hour,
# MAGIC     CAST(SUBSTRING(time, 7, 2) AS INT) AS second_of_minute,
# MAGIC     CASE
# MAGIC         WHEN CAST(SUBSTRING(time, 1, 2) AS INT) BETWEEN 5 AND 11 THEN 'Morning'
# MAGIC         WHEN CAST(SUBSTRING(time, 1, 2) AS INT) BETWEEN 12 AND 16 THEN 'Afternoon'
# MAGIC         WHEN CAST(SUBSTRING(time, 1, 2) AS INT) BETWEEN 17 AND 20 THEN 'Evening'
# MAGIC         ELSE 'Night'
# MAGIC     END AS time_period
# MAGIC FROM bronze_wind_power;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * FROM transformed_wind_power


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Drop the wind_power table in the Silver Lakehouse if it exists
# MAGIC DROP TABLE IF EXISTS repo_wind.LH_To_Silver_wind.dbo.wind_power;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Create the new wind_power table in Silver Lakehouse
# MAGIC CREATE TABLE repo_wind.LH_To_Silver_wind.dbo.wind_powe
# MAGIC USING delta
# MAGIC AS
# MAGIC SELECT * FROM transformed_wind_power;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

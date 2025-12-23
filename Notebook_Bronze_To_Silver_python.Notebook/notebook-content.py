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

from pyspark.sql.functions import round, col, dayofmonth, month, year, to_date, quarter, substring, when, regexp_replace

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#Path to wind_power table in bronze lakehouse
bronze_table_path = "abfss://repo_wind@onelake.dfs.fabric.microsoft.com/wind_bronze.Lakehouse/Tables/dbo/wind_table"

#load wind_power table into dataframe
df = spark.read.format("delta").load(bronze_table_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Clean and enrich data
df_transformed = (df
    .withColumn("wind_speed", round(col("wind_speed"), 2))
    .withColumn("energy_produced", round(col("energy_produced"), 2))
    .withColumn("day", dayofmonth(col("date")))
    .withColumn("month", month(col("date")))
    .withColumn("quarter", quarter(col("date")))
    .withColumn("year", year(col("date")))
    .withColumn("time", regexp_replace(col("time"), "-", ":"))
    .withColumn("hour_of_day", substring(col("time"), 1, 2).cast("int"))
    .withColumn("minute_of_hour", substring(col("time"), 4, 2).cast("int"))
    .withColumn("second_of_minute", substring(col("time"), 7, 2).cast("int"))
    .withColumn("time_period", when((col("hour_of_day") >= 5) & (col("hour_of_day") < 12), "Morning")
                                .when((col("hour_of_day") >= 12) & (col("hour_of_day") < 17), "Afternoon")
                                .when((col("hour_of_day") >= 17) & (col("hour_of_day") < 21), "Evening")
                                .otherwise("Night")
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Path to wind_power table in Silver Lakehouse
silver_table_path = "abfss://repo_wind@onelake.dfs.fabric.microsoft.com/LH_To_Silver_wind.Lakehouse/Tables/dbo/wind_power"
df_transformed.write.format("delta").mode("overwrite").save(silver_table_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

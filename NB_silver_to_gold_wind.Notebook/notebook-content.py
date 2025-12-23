# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "69255059-660d-42ba-814d-5651d7c62dab",
# META       "default_lakehouse_name": "LH_To_Silver_wind",
# META       "default_lakehouse_workspace_id": "00e69122-80e7-4974-8e82-5e52582fc33c",
# META       "known_lakehouses": [
# META         {
# META           "id": "69255059-660d-42ba-814d-5651d7c62dab"
# META         },
# META         {
# META           "id": "5a8a8a4d-a0cc-4904-a1bf-431968a96b9a"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.window import Window
from pyspark.sql.functions import row_number
from pyspark.sql.functions import explode, sequence, to_date, year, month, quarter, dayofmonth, dayofweek, date_format

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#path to wind_power table in Silver lakehouse
silver_table_path = "abfss://repo_wind@onelake.dfs.fabric.microsoft.com/LH_To_Silver_wind.Lakehouse/Tables/dbo/wind_power"

#load the wind_power table into a dataframe
df = spark.read.format("delta").load(silver_table_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create the Date Dimension Table
date_dim = df.select("date", "day", "month", "quarter", "year").distinct() \
                .withColumnRenamed("date", "date_id")

# Create the Time Dimension Table
time_dim = df.select("time", "hour_of_day", "minute_of_hour", "second_of_minute", "time_period").distinct() \
                .withColumnRenamed("time", "time_id")

# Create the Turbine Dimension Table
turbine_dim = df.select("turbine_name", "capacity", "location_name", "latitude", "longitude", "region").distinct() \
                .withColumn("turbine_id", row_number().over(Window.orderBy("turbine_name", "capacity", "location_name", "latitude", "longitude", "region")))

# Create the Operational Status Dimension Table
operational_status_dim = df.select("status", "responsible_department").distinct() \
                .withColumn("status_id", row_number().over(Window.orderBy("status", "responsible_department")))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#join the dimension tables to the original dataframe
df = df.join(turbine_dim, ["turbine_name", "capacity", "location_name", "latitude", "longitude", "region"], "left") \
        .join(operational_status_dim, ["status", "responsible_department"], "left")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#create the fact table
fact_table = df.select("production_id", "date", "time", "turbine_id", "status_id", "wind_speed", "wind_direction", "energy_produced") \
                .withColumnRenamed("date", "date_id") \
                .withColumnRenamed("time", "time_id")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#path to the Gold tables

gold_date_dim_path = "abfss://repo_wind@onelake.dfs.fabric.microsoft.com/LH_Wind_Gold.Lakehouse/Tables/dbo/dim_date"
gold_time_dim_path = "abfss://repo_wind@onelake.dfs.fabric.microsoft.com/LH_Wind_Gold.Lakehouse/Tables/dbo/dim_time"
gold_turbine_dim_path = "abfss://repo_wind@onelake.dfs.fabric.microsoft.com/LH_Wind_Gold.Lakehouse/Tables/dbo/dim_turbine"
gold__operational_status_dim_path = "abfss://repo_wind@onelake.dfs.fabric.microsoft.com/LH_Wind_Gold.Lakehouse/Tables/dbo/dim_operational_status"
gold_fact_table_path = "abfss://repo_wind@onelake.dfs.fabric.microsoft.com/LH_Wind_Gold.Lakehouse/Tables/dbo/fact_wind_power"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#sauvegarde dans le lakehouse gold
date_dim.write.format("delta").mode("overwrite").save(gold_date_dim_path)
time_dim.write.format("delta").mode("overwrite").save(gold_time_dim_path)
turbine_dim.write.format("delta").mode("overwrite").save(gold_turbine_dim_path)
operational_status_dim.write.format("delta").mode("overwrite").save(gold__operational_status_dim_path)
fact_table.write.format("delta").mode("overwrite").save(gold_fact_table_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

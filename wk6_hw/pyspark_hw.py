import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .config("spark.ui.port", "4040") \
    .getOrCreate()

df = spark.read.parquet('data/yellow_tripdata_2025-11.parquet')
print("df read")

#df = df.repartition(4)
#print("df repartitioned")
#
#df.write.mode('overwrite').parquet('data/partitioned')

from pyspark.sql import functions as F
print(df.columns)
#print(df.filter(
#            (F.col("tpep_pickup_datetime") >= '2025-11-15')& 
#            (F.col("tpep_pickup_datetime") < '2025-11-16')
#            ).count()
#)

#df = df \
#    .withColumn('tpep_pickup_datetime', F.to_timestamp('tpep_pickup_datetime', "yyyy-MM-dd HH:mm:ss")) \
#    .withColumn('tpep_dropoff_datetime', F.to_timestamp('tpep_dropoff_datetime', "yyyy-MM-dd HH:mm:ss"))
#
#df = df \
#    .withColumn('duration', F.col('tpep_dropoff_datetime') - F.col('tpep_pickup_datetime')) \
#    .withColumn('duration', F.round((F.col('duration').cast('int'))/3600, 1))
#
#print(df.select(F.max(F.col('duration'))).show())
zone = spark.read.csv('data/taxi_zone_lookup.csv', header=True)

df_zone = df \
    .filter(
        (F.col("tpep_pickup_datetime") >= '2025-11-01')& 
        (F.col("tpep_pickup_datetime") < '2025-12-01')
    ) \
    .join(zone, df.PULocationID == zone.LocationID, 'left') \
    .groupBy('Zone') \
    .agg(F.count('*').alias('count')) \
    .sort('count', ascending=True) \
    .show()

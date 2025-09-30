from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("example") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
df = spark.createDataFrame(data, ["name", "age"])
df.show()
spark.stop()

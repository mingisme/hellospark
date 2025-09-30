# Hello Spark

## Requirements
- Docker and Docker Compose installed

## Start Spark cluster
```bash
docker compose up -d
```

- Spark master UI: http://localhost:8080
- Spark worker UI: http://localhost:8081

## Submit the example job
The compose file mounts the current directory at `/opt/spark-apps` in the containers.

Run the example from the worker (or master) container:
```bash
docker cp -L example.py spark-master:/opt/spark/work-dir/example.py

docker exec -it spark-master bash -lc "/opt/spark/bin/spark-submit --conf spark.jars.ivy=/tmp/.ivy  --master spark://spark-master:7077 /opt/spark/work-dir/example.py"
```

## go into spark-master
docker exec -it spark-master bash

## open pyspark
pyspark

## run example
```python
from pyspark import SparkContext 

sc = SparkContext("local", "RDD Example")

data = [1, 2, 3, 4, 5]
rdd = sc.parallelize(data)

squared_rdd = rdd.map(lambda x: x * x)

results = squared_rdd.collect()
print(results)
```

## dataframes
```python
from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder.appName("DataFrame Example").getOrCreate()

# Create a DataFrame from a list of tuples
data = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, columns)

# Show the DataFrame
df.show()

filtered_df = df.filter(df["Age"] > 30)
filtered_df.show()

selected_df = df.select("Name")
selected_df.show()

grouped_df = df.groupBy("Name").agg({"Age": "avg"})
grouped_df.show()
```

## spark SQL
```python
spark = SparkSession.builder.appName("Spark SQL example").getOrCreate()

df = spark.createDataFrame([
    (1, "Elon Musk", 25),
    (2, "Larry Page", 30),
    (3, "Jeff Bezos", 35),
    (4, "Jeff Bezos", 45)
], ["id", "name", "age"])

df.createOrReplaceTempView("people")

result = spark.sql("SELECT * FROM people WHERE age > 28")
result.show()
```


## Spark streaming
```python

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Initialize SparkContext
sc = SparkContext.getOrCreate()

# Creating a StreamingContext with a batch interval of 1 second
ssc = StreamingContext(sc, 1)

# Creating a DStream to read lines from the standard input
lines = ssc.textFileStream("/opt/spark/work-dir/example.py")

# Count the words in each line
counts = lines.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

# Print the word counts every 5 seconds
counts.pprint(5)

# Start the streaming computation
ssc.start()

# Keep the main thread running to prevent the program from exiting
ssc.awaitTermination()

```



## Stop the cluster
```bash
docker compose down
```
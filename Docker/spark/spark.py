from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

# Initialize Spark Session (dependencies assumed to be configured)
spark = SparkSession.builder.appName("KafkaStreamingRead").getOrCreate()

# Read from Kafka
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "house_data") \
    .option("startingOffsets", "latest") \
    .load()

# The Kafka DataFrame will have columns like 'key', 'value', 'topic', 'partition', 'offset', and 'timestamp'
# 'key' and 'value' are in binary format, so you often need to cast them to strings
processed_df = kafka_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Start the streaming query to a sink (e.g., console for demonstration)
query = processed_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()

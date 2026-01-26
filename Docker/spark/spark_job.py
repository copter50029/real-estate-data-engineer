import pyspark
import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, DoubleType , BooleanType , ShortType , TimestampType
from pyspark.sql.functions import from_json, col,regexp_replace, to_timestamp


if __name__ == "__main__":
    spark = SparkSession.builder \
    .appName("KafkaFraudDetectionStream") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-streaming-kafka-0-10_2.13:4.0.0,org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0") \
    .config("spark.jars", "/opt/spark/apps/postgresql-42.7.9.jar") \
    .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    first_run = True
    # 2. Define schema for Kafka JSON messages (all fields from your item)
    schema = StructType([
    StructField("id", StringType()),
    StructField("rawHomeStatusCd", StringType()),
    StructField("marketingStatusSimplifiedCd", StringType()),
    StructField("hasImage",BooleanType()), 
    StructField("statusType",StringType()),
    StructField("price",LongType()),
    StructField("isUndisclosedAddress",BooleanType()),
    StructField("shouldShowRequestOnPrice",BooleanType()),
    StructField("bedrooms",ShortType()),
    StructField("bathrooms",ShortType()),
    StructField("area",IntegerType()),
    StructField("isZillowOwned",BooleanType()),
    StructField("contentType", StringType()),
    StructField("latitude", DoubleType()),
    StructField("longitude", DoubleType()),
    StructField("streetAddress", StringType()),
    StructField("zipcode", StringType()),
    StructField("city", StringType()),
    StructField("state", StringType()),
    StructField("livingArea", IntegerType()),
    StructField("homeType", StringType()),
    StructField("homeStatus", StringType()),
    StructField("daysOnZillow", IntegerType()),
    StructField("isFeatured", BooleanType()),
    StructField("shouldHighlight", BooleanType()),
    StructField("zestimate", LongType()),
    StructField("rentZestimate", LongType()),
    StructField("is_FSBA", BooleanType()),
    StructField("is_openHouse", BooleanType()),
    StructField("openHouse", StringType()),
    StructField("isUnmappable", BooleanType()),
    StructField("isPreforeclosureAuction", BooleanType()),
    StructField("homeStatusForHDP", StringType()),
    StructField("priceForHDP", LongType()),
    StructField("timeOnZillow", LongType()),
    StructField("isNonOwnerOccupied", BooleanType()),
    StructField("isPremierBuilder", BooleanType()),
    StructField("currency", StringType()),
    StructField("country", StringType()),
    StructField("taxAssessedValue", LongType()),
    StructField("lotAreaValue", DoubleType()),
    StructField("lotAreaUnit", StringType()),
    StructField("isShowcaseListing", BooleanType()),
    StructField("isSaved", BooleanType()),
    StructField("isUserClaimingOwner", BooleanType()),
    StructField("isUserConfirmedClaim", BooleanType()),
    StructField("zestimate_top", LongType()),
    StructField("shouldShowZestimateAsPrice", BooleanType()),
    StructField("has3DModel", BooleanType()),
    StructField("hasVideo", BooleanType()),
    StructField("isHomeRec", BooleanType()),
    StructField("hasAdditionalAttributions", BooleanType()),
    StructField("isFeaturedListing", BooleanType()),
    StructField("isShowcaseListing_top", BooleanType()),
    StructField("info6String", StringType()),
    StructField("brokerName", StringType()),
    StructField("hasOpenHouse", BooleanType()),
    StructField("openHouseStartDate", TimestampType()),
    StructField("openHouseEndDate", TimestampType()),
    StructField("isPaidBuilderNewConstruction", BooleanType()),
    StructField("imgSrc", StringType())
    ])

    # 3. Read from Kafka topic
    if first_run:
        kafka_df = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "broker1:29292") \
            .option("subscribe", "house_data") \
            .option("checkpointLocation", "/tmp/spark_checkpoints/kafka_log") \
            .option("startingOffsets", "earliest") \
            .load()
        first_run = False
    else:
        kafka_df = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "broker1:29292") \
            .option("subscribe", "house_data") \
            .option("checkpointLocation", "/tmp/spark_checkpoints/kafka_log") \
            .option("startingOffsets", "latest") \
            .load()
        
    parsed_df = kafka_df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")
    parsed_df = parsed_df.withColumn("openHouseStartDate", regexp_replace(col("openHouseStartDate"), "T", " "))
    parsed_df = parsed_df.withColumn("openHouseEndDate", regexp_replace(col("openHouseEndDate"), "T", " "))

    parsed_df = parsed_df.withColumn("openHouseStartDate", to_timestamp(col("openHouseStartDate"), "yyyy-MM-dd HH:mm:ss"))
    parsed_df = parsed_df.withColumn("openHouseEndDate", to_timestamp(col("openHouseEndDate"), "yyyy-MM-dd HH:mm:ss"))

    table_name = "real_estate"
    jdbc_url = "jdbc:postgresql://real-estate-postgres:5432/real_estate_db"

    def write_to_postgres(batch_df, batch_id):
        batch_df.write.format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", table_name) \
            .option("user", "admin") \
            .option("password", "admin") \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()

    query = parsed_df.writeStream \
        .foreachBatch(write_to_postgres) \
        .outputMode("append") \
        .start()

    query.awaitTermination()
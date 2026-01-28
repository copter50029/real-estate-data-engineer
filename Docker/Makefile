submit-spark-job:
	docker exec da-spark-master spark-submit --master spark://spark-master:7077 --packages \
	org.apache.spark:spark-streaming-kafka-0-10_2.13:4.0.0,\
	org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0  \
	--jars apps/postgresql-42.7.9.jar \
	apps/spark_job.py
turn-on-dag:
	docker exec docker-airflow-apiserver-1 airflow dags unpause Zillow_Scraper
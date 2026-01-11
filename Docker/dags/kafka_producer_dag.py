from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from kafka import KafkaProducer
from datetime import datetime, timedelta
import json
import logging
import time
from scraper import get_listings, us_states
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
}


def main():
    producer = KafkaProducer(
        bootstrap_servers=["broker1:29292"],
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        acks='all',  # Wait for all replicas to acknowledge
        retries=3,   # Retry failed sends
        max_in_flight_requests_per_connection=1  # Ensure ordering
    )
    for i in range(41):
        data= get_listings(us_states[i], 1)
        for listing in data:
            producer.send("house_data", value=listing)
            logging.info(f"Sent: {listing}")
        time.sleep(5)


with DAG(
    "Zillow_Scraper",
    default_args=default_args,
    description="Scrapes Zillow data and sends it to Kafka",
    schedule=timedelta(minutes=1),
    start_date=datetime.now(),
    catchup=False,
) as dag:
    produce_task = PythonOperator(
        task_id="Zillow_Scraper",
        python_callable=main,
    )

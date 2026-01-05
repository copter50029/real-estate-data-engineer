from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from kafka import KafkaProducer
from datetime import datetime, timedelta
import json
import logging
import time

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
}


def main():
    producer = KafkaProducer(
        bootstrap_servers=["broker1:29092"],
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )
    for i in range(10):
        data = (
            {
                "zpid": "2073776159",
                "palsId": "12004_73444380",
                "id": "2073776159",
                "rawHomeStatusCd": "ForSale",
                "marketingStatusSimplifiedCd": "For Sale by Agent",
                "imgSrc": "https://photos.zillowstatic.com/fp/ce1b4f875bc7bf572f9fe82d1211815b-p_e.jpg",
                "hasImage": True,
                "detailUrl": "https://www.zillow.com/homedetails/1-Lewis-Wharf-Boston-MA-02110/2073776159_zpid/",
                "statusType": "FOR_SALE",
                "statusText": "House for sale",
                "countryCurrency": "$",
                "price": "$450,000",
                "unformattedPrice": 450000,
                "address": "1 Lewis Wharf, Boston, MA 02110",
                "addressStreet": "1 Lewis Wharf",
                "addressCity": "Boston",
                "addressState": "MA",
                "addressZipcode": "02110",
                "isUndisclosedAddress": False,
                "shouldShowRequestOnPrice": False,
                "beds": 2,
                "baths": 2,
                "area": 700,
                "latLong": {"latitude": 42.363537, "longitude": -71.05128},
                "isZillowOwned": False,
                "flexFieldText": "52 days on Zillow",
                "contentType": "daysOnZillow",
                "hdpData": {
                    "homeInfo": {
                        "zpid": 2073776159,
                        "streetAddress": "1 Lewis Wharf",
                        "zipcode": "02110",
                        "city": "Boston",
                        "state": "MA",
                        "latitude": 42.363537,
                        "longitude": -71.05128,
                        "price": 450000,
                        "bathrooms": 2,
                        "bedrooms": 2,
                        "livingArea": 700,
                        "homeType": "SINGLE_FAMILY",
                        "homeStatus": "FOR_SALE",
                        "daysOnZillow": 52,
                        "isFeatured": False,
                        "shouldHighlight": False,
                        "rentZestimate": 4512,
                        "listing_sub_type": {"is_FSBA": True},
                        "isUnmappable": False,
                        "isPreforeclosureAuction": False,
                        "homeStatusForHDP": "FOR_SALE",
                        "priceForHDP": 450000,
                        "timeOnZillow": 4498113000,
                        "isNonOwnerOccupied": True,
                        "isPremierBuilder": False,
                        "isZillowOwned": False,
                        "currency": "USD",
                        "country": "USA",
                        "lotAreaValue": 0,
                        "lotAreaUnit": "sqft",
                        "isShowcaseListing": False,
                    }
                },
                "isSaved": False,
                "isUserClaimingOwner": False,
                "isUserConfirmedClaim": False,
                "pgapt": "ForSale",
                "sgapt": "For Sale (Broker)",
                "shouldShowZestimateAsPrice": False,
                "has3DModel": False,
                "hasVideo": False,
                "isHomeRec": False,
                "hasAdditionalAttributions": True,
                "isFeaturedListing": False,
                "isShowcaseListing": False,
                "list": True,
                "relaxed": False,
                "info6String": "Sarah Fillmann",
                "brokerName": "Coldwell Banker Realty - Boston",
                "carouselPhotosComposable": {
                    "baseUrl": "https://photos.zillowstatic.com/fp/{photoKey}-p_e.jpg",
                    "communityBaseUrl": "Null",
                    "photoData": [
                        {
                            "photoKey": "ce1b4f875bc7bf572f9fe82    parsed = json.load(f)d1211815b"
                        },
                        {"photoKey": "41f21580f465c4e3bb5f96108392047c"},
                        {"photoKey": "0d81caf733a3caad6d71795bc9ae4142"},
                        {"photoKey": "d75429650593bece90d4abb2dd95168e"},
                    ],
                    "communityPhotoData": "Null",
                    "isStaticUrls": False,
                },
                "isPaidBuilderNewConstruction": False,
            },
        )

        producer.send("house_data", value=data)
        logging.info(f"Sent: {data}")
        time.sleep(1)


with DAG(
    "kafka_producer",
    default_args=default_args,
    description="A simple DAG to produce dummy Kafka json data",
    schedule=timedelta(minutes=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    produce_task = PythonOperator(
        task_id="produce_dummy_data",
        python_callable=main,
    )

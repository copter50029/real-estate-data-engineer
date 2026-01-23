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


def  extract(producer_task):
    data= get_listings(us_states[producer_task], 1)
    return data

def get_structure(data):

    producer = KafkaProducer(
        bootstrap_servers=["broker1:29292"],
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        acks='all',  # Wait for all replicas to acknowledge
        retries=3,   # Retry failed sends
        max_in_flight_requests_per_connection=1  # Ensure ordering
    )
    def get_nested(data, keys):
        try:
            for key in keys:
                data = data[key]
            return data
        except (KeyError, TypeError):
            return None
    for i in range(len(data)):   
        schema = {}
        schema["rawHomeStatusCd"] = data[i].get("rawHomeStatusCd")
        schema["marketingStatusSimplifiedCd"] = data[i].get("marketingStatusSimplifiedCd")
        schema["imgSrc"] = data[i].get("imgSrc")
        schema["hasImage"] = data[i].get("hasImage")
        schema["detailUrl"] = data[i].get("detailUrl")
        schema["statusType"] = data[i].get("statusType")
        schema["statusText"] = data[i].get("statusText")
        schema["countryCurrency"] = data[i].get("countryCurrency")
        schema["price"] = data[i].get("price")
        schema["unformattedPrice"] = data[i].get("unformattedPrice")
        schema["address"] = data[i].get("address")
        schema["addressStreet"] = data[i].get("addressStreet")
        schema["addressCity"] = data[i].get("addressCity")
        schema["addressState"] = data[i].get("addressState")
        schema["addressZipcode"] = data[i].get("addressZipcode")
        schema["isUndisclosedAddress"] = data[i].get("isUndisclosedAddress")
        schema["shouldShowRequestOnPrice"] = data[i].get("shouldShowRequestOnPrice")
        schema["beds"] = data[i].get("beds")
        schema["baths"] = data[i].get("baths")
        schema["area"] = data[i].get("area")
        schema["isZillowOwned"] = data[i].get("isZillowOwned")
        schema["flexFieldText"] = data[i].get("flexFieldText")
        schema["contentType"] = data[i].get("contentType")
        schema["latitude"] = get_nested(data[i], ["latLong", "latitude"])
        schema["longitude"] = get_nested(data[i], ["latLong", "longitude"])
        schema["streetAddress"] = get_nested(data[i], ["hdpData", "homeInfo", "streetAddress"])
        schema["zipcode"] = get_nested(data[i], ["hdpData", "homeInfo", "zipcode"])
        schema["city"] = get_nested(data[i], ["hdpData", "homeInfo", "city"])
        schema["state"] = get_nested(data[i], ["hdpData", "homeInfo", "state"])
        schema["latitude"] = get_nested(data[i], ["hdpData", "homeInfo", "latitude"])
        schema["longitude"] = get_nested(data[i], ["hdpData", "homeInfo", "longitude"])
        schema["price"] = get_nested(data[i], ["hdpData", "homeInfo", "price"])
        schema["bathrooms"] = get_nested(data[i], ["hdpData", "homeInfo", "bathrooms"])
        schema["bedrooms"] = get_nested(data[i], ["hdpData", "homeInfo", "bedrooms"])
        schema["livingArea"] = get_nested(data[i], ["hdpData", "homeInfo", "livingArea"])
        schema["homeType"] = get_nested(data[i], ["hdpData", "homeInfo", "homeType"])
        schema["homeStatus"] = get_nested(data[i], ["hdpData", "homeInfo", "homeStatus"])
        schema["daysOnZillow"] = get_nested(data[i], ["hdpData", "homeInfo", "daysOnZillow"])
        schema["isFeatured"] = get_nested(data[i], ["hdpData", "homeInfo", "isFeatured"])
        schema["shouldHighlight"] = get_nested(data[i], ["hdpData", "homeInfo", "shouldHighlight"])
        schema["zestimate"] = get_nested(data[i], ["hdpData", "homeInfo", "zestimate"])
        schema["rentZestimate"] = get_nested(data[i], ["hdpData", "homeInfo", "rentZestimate"])
        schema["is_FSBA"] = get_nested(data[i], ["hdpData", "homeInfo", "listing_sub_type", "is_FSBA"])
        schema["is_openHouse"] = get_nested(data[i], ["hdpData", "homeInfo", "listing_sub_type", "is_openHouse"])
        schema["openHouse"] = get_nested(data[i], ["hdpData", "homeInfo", "openHouse"])
        schema["isUnmappable"] = get_nested(data[i], ["hdpData", "homeInfo", "isUnmappable"])
        schema["isPreforeclosureAuction"] = get_nested(data[i], ["hdpData", "homeInfo", "isPreforeclosureAuction"])
        schema["homeStatusForHDP"] = get_nested(data[i], ["hdpData", "homeInfo", "homeStatusForHDP"])
        schema["priceForHDP"] = get_nested(data[i], ["hdpData", "homeInfo", "priceForHDP"])
        schema["timeOnZillow"] = get_nested(data[i], ["hdpData", "homeInfo", "timeOnZillow"])
        schema["isNonOwnerOccupied"] = get_nested(data[i], ["hdpData", "homeInfo", "isNonOwnerOccupied"])
        schema["isPremierBuilder"] = get_nested(data[i], ["hdpData", "homeInfo", "isPremierBuilder"])
        schema["isZillowOwned"] = get_nested(data[i], ["hdpData", "homeInfo", "isZillowOwned"])
        schema["currency"] = get_nested(data[i], ["hdpData", "homeInfo", "currency"])
        schema["country"] = get_nested(data[i], ["hdpData", "homeInfo", "country"])
        schema["taxAssessedValue"] = get_nested(data[i], ["hdpData", "homeInfo", "taxAssessedValue"])
        schema["lotAreaValue"] = get_nested(data[i], ["hdpData", "homeInfo", "lotAreaValue"])
        schema["lotAreaUnit"] = get_nested(data[i], ["hdpData", "homeInfo", "lotAreaUnit"])
        schema["isShowcaseListing"] = get_nested(data[i], ["hdpData", "homeInfo", "isShowcaseListing"])
        schema["isSaved"] = data[i].get("isSaved")
        schema["isUserClaimingOwner"] = data[i].get("isUserClaimingOwner")
        schema["isUserConfirmedClaim"] = data[i].get("isUserConfirmedClaim")
        schema["pgapt"] = data[i].get("pgapt")
        schema["sgapt"] = data[i].get("sgapt")
        schema["zestimate_top"] = data[i].get("zestimate")
        schema["shouldShowZestimateAsPrice"] = data[i].get("shouldShowZestimateAsPrice")
        schema["has3DModel"] = data[i].get("has3DModel")
        schema["hasVideo"] = data[i].get("hasVideo")
        schema["isHomeRec"] = data[i].get("isHomeRec")
        schema["hasAdditionalAttributions"] = data[i].get("hasAdditionalAttributions")
        schema["isFeaturedListing"] = data[i].get("isFeaturedListing")
        schema["isShowcaseListing_top"] = data[i].get("isShowcaseListing")
        schema["list"] = data[i].get("list")
        schema["relaxed"] = data[i].get("relaxed")
        schema["info6String"] = data[i].get("info6String")
        schema["brokerName"] = data[i].get("brokerName")
        schema["hasOpenHouse"] = data[i].get("hasOpenHouse")
        schema["openHouseStartDate"] = data[i].get("openHouseStartDate")
        schema["openHouseEndDate"] = data[i].get("openHouseEndDate")
        schema["openHouseDescription"] = data[i].get("openHouseDescription")
        schema["isPaidBuilderNewConstruction"] = data[i].get("isPaidBuilderNewConstruction")
        producer.send("house_data", value=schema)
        logging.info(f"Sent data to Kafka: {schema}")
    producer.flush()
    producer.close()
with DAG(
    "Zillow_Scraper",
    default_args=default_args,
    description="Scrapes Zillow data and sends it to Kafka",
    schedule =timedelta(days=1),
    start_date=datetime.now(),
    catchup=False,
    # max task for dag it limit scraper to run at the same time for avoid bot detection
    max_active_tasks=2,
) as dag:
    for producer_task in range(41):
        name = us_states[producer_task]['name'].replace(" ", "_")
        produce_task = PythonOperator(
            task_id=f"Zillow_Scraper_{name}",
            python_callable=extract,
            op_args=[producer_task],
        )
        get_structure_task = PythonOperator(
            task_id=f"Get_Structure_{name}",
            python_callable=get_structure,
            op_args=[produce_task.output],

        )

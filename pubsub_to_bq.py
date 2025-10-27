import base64
import csv
import logging
from google.cloud import bigquery, pubsub_v1

# BigQuery setup
BQ_TABLE_ID = "playground-s-11-a324b2b9.Neptune.cust_data"
bq_client = bigquery.Client()


def pubsub_to_bq_and_relay(event, context):
    """
    Triggered by Pub/Sub subscription from source project.
    Inserts CSV messages into BigQuery and republishes them to another topic.
    """
    try:
        # Decode Pub/Sub message
        pubsub_message = base64.b64decode(event['data']).decode('utf-8').strip()
        logging.info(f"Received message: {pubsub_message}")

        # Parse CSV message
        reader = csv.reader([pubsub_message])
        for row in reader:
            if len(row) != 7:
                logging.error(f"Unexpected number of columns: {row}")
                return
            row_dict = {
                "id": row[0],
                "ipaddress": row[1],
                "action": row[2],
                "accountnumber": row[3],
                "actionid": int(row[4]),
                "name": row[5],
                "actionby": row[6]
            }

            # Insert into BigQuery
            errors = bq_client.insert_rows_json(BQ_TABLE_ID, [row_dict])
            if errors:
                logging.error(f"BigQuery insert errors: {errors}")
            else:
                logging.info(f"Inserted into BigQuery: {row_dict}")


    except Exception as e:
        logging.exception(f"Error processing message: {e}")

import base64
import csv
import logging
from google.cloud import bigquery
from flask import Flask, request

# BigQuery setup
BQ_TABLE_ID = "playground-s-11-a324b2b9.Neptune.cust_data"
bq_client = bigquery.Client()

def pubsub_to_bq(request):
    """
    Cloud Function HTTP endpoint triggered by Pub/Sub push.
    Inserts CSV messages into BigQuery.
    """
    try:
        envelope = request.get_json()
        if not envelope:
            msg = "No Pub/Sub message received"
            logging.error(msg)
            return msg, 400

        if 'message' not in envelope:
            msg = "Invalid Pub/Sub message format"
            logging.error(msg)
            return msg, 400

        pubsub_message = base64.b64decode(envelope['message']['data']).decode('utf-8').strip()
        logging.info(f"Received message: {pubsub_message}")

        # Parse CSV message
        reader = csv.reader([pubsub_message])
        for row in reader:
            if len(row) != 7:
                logging.error(f"Unexpected number of columns: {row}")
                continue

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

        return "OK", 200

    except Exception as e:
        logging.exception(f"Error processing message: {e}")
        return f"Error: {e}", 500

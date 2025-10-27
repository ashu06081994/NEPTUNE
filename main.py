import base64
import csv
import logging
from google.cloud import bigquery
from flask import Flask, request
from markupsafe import escape


BQ_TABLE_ID = "playground-s-11-a324b2b9.Neptune.cust_data"
bq_client = bigquery.Client()

def pubsub_to_bq(request):
    """
    HTTP Cloud Function triggered by Pub/Sub push.
    """
    try:
        # Ensure request is JSON
        envelope = request.get_json(silent=True)
        if envelope is None:
            logging.error("No JSON payload received")
            return "Bad Request: No JSON", 400

        if 'message' not in envelope:
            logging.error(f"Invalid Pub/Sub message format: {envelope}")
            return "Bad Request: Missing 'message' field", 400

        message = envelope['message']

        # Decode base64 data
        if 'data' not in message:
            logging.error(f"No data in message: {message}")
            return "Bad Request: Missing 'data' field", 400

        pubsub_message = base64.b64decode(message['data']).decode('utf-8').strip()
        logging.info(f"Received message: {pubsub_message}")

        # Parse CSV
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

            errors = bq_client.insert_rows_json(BQ_TABLE_ID, [row_dict])
            if errors:
                logging.error(f"BigQuery insert errors: {errors}")
            else:
                logging.info(f"Inserted into BigQuery: {row_dict}")

        return "OK", 200

    except Exception as e:
        logging.exception(f"Error processing message: {e}")
        return f"Internal Server Error: {escape(str(e))}", 500

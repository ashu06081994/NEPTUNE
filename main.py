from flask import Flask, request
from markupsafe import escape
import base64
from google.cloud import bigquery
import logging

app = Flask(__name__)
table_id = "Neptune.rawmessages"  # BigQuery table

@app.route("/", methods=["POST"])
def pubsub_to_bq():
    envelope = request.get_json(silent=True)
    if envelope is None:
        logging.error("No JSON payload received")
        return "Bad Request: No JSON", 400

    # Extract Pub/Sub message
    pubsub_message = envelope.get("message")
    if pubsub_message is None:
        logging.error("No 'message' field in request")
        return "Bad Request: No message", 400

    data = base64.b64decode(pubsub_message.get("data", "")).decode("utf-8")
    logging.info(f"Row to insert: {data}")

    # Insert into BigQuery
    client = bigquery.Client()
    table = client.get_table(table_id)

    # Split CSV line to match your schema
    try:
     
        row_to_insert = [(data,)]     # NOTE - the trailing comma is required for this case - it expects a tuple
        errors = client.insert_rows(table, row_to_insert)
        if errors:
            logging.error(f"BigQuery insert errors: {errors}")
            return f"Error inserting into BigQuery: {errors}", 500
    except Exception as e:
        logging.error(f"Error processing message here after try: {e}")
        return f"Error processing message: {e}", 500

    return "OK", 200

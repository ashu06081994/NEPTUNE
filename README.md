# NEPTUNE
PROJECT FOR PDE
a. pre-project.sh: We are setting up the project and service account details.Also enabling the api's required. Then creating the topic and subscription. Deploying the cloud function as well.
b. main.py: This file is the code for cloud function to push the data recieved by the topic to bigquery.

Issues:
i. The subscription created in student project  to push the data to the topic in student project is receiving the data from moonbank-neptune/activities but the topic in student is not receiving the data by push mechanism. Tried to debug it using many different ways but it seems to not work.

Steps to execute:
1. Run pre-project.sh to install the pre-requisites and deploy the cloud function.

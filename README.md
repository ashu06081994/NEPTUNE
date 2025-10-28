# NEPTUNE
PROJECT FOR PDE <br>
* pre-project.sh: We are setting up the project and service account details.Also enabling the api's required.<br>
Then creating the topic and subscription. Deploying the cloud function as well.
* main.py: This file is the code for cloud function to push the data recieved by the topic to bigquery.

Issues:
* The subscription created in student project  to push the data to the topic in student project is receiving the data from moonbank-neptune/activities but the topic in student is not receiving the data by push mechanism. Tried to debug it using many different ways but it seems to not work.

Steps to execute:
* Run pre-project.sh to install the pre-requisites and deploy the cloud function.

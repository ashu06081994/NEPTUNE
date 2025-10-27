
# creating the topic in current project
gcloud pubsub topics create neptune-activities

#creating the subscription in current project
gcloud pubsub subscriptions create neptune-activities-test --topic neptune-activities

#attaching the above subscription to neptune project topic to get the data

gcloud pubsub subscriptions create neptune-activities --topic projects/moonbank-neptune/topics/activities --push-endpoint=https://pubsub.googleapis.com/v1/projects/$GOOGLE_CLOUD_PROJECT/topics/neptune-activities:publish 

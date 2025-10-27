PROJECT_ID=$(gcloud config get-value project)
export PROJECT_NUMBER=$(gcloud projects list --filter="$PROJECT_ID" --format="value(PROJECT_NUMBER)")
export serviceAccount=""$PROJECT_NUMBER"-compute@developer.gserviceaccount.com"



gcloud services enable cloudfunctions.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable eventarc.googleapis.com

bq mk neptune
bq mk --schema message:STRING -t neptune.rawmessages

gcloud pubsub topics create activities-topic --project=$GOOGLE_CLOUD_PROJECT


gcloud pubsub subscriptions create activities-subscription \
    --topic=projects/moonbank-neptune/topics/activities \
    --push-endpoint="https://pubsub.googleapis.com/v1/projects/$GOOGLE_CLOUD_PROJECT/topics/activities-topic:publish"  

    
gcloud functions deploy processActivities \
    --runtime python310 \
    --trigger-topic activities-topic \
    --entry-point process_message \
    --project=playground-s-11-a324b2b9 \
    --region=us-central1

    gcloud functions deploy processActivities \     
           --runtime python310 \    
           --trigger-topic activities-topic \    
           --entry-point pubsub_to_bq   \   
           --project=$GOOGLE_CLOUD_PROJECT   \  
           --region=us-central1 \
           --source .

# gcloud pubsub topics publish activities-topic --message="new_account: test user" -- to manually push a message

# deploying cloud function
# gcloud functions deploy pubsub_to_bq \
#     --runtime python310 \
#     --trigger-http \
#     --entry-point pubsub_to_bq \
#     --project $GOOGLE_CLOUD_PROJECT \
#     --region us-central1 \
#     --source . \
#     --allow-unauthenticated
    
# sleep 240

# #creating the subscription in current project to push data to bq
# gcloud pubsub subscriptions create neptune-activities-push \
#     --topic projects/moonbank-neptune/topics/activities \
#     --push-endpoint=https://us-central1-$GOOGLE_CLOUD_PROJECT.cloudfunctions.net/pubsub_to_bq \
#     --ack-deadline=30 \
#     --project $GOOGLE_CLOUD_PROJECT

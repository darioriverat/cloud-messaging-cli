import os
from google.cloud import pubsub_v1
from dotenv import load_dotenv
import argparse

os.environ.clear()
load_dotenv()

# Set up argument parser
parser = argparse.ArgumentParser(description='Argument parser for pubsub.')
parser.add_argument('--create-topic', type=str, help='Name of the topic to create')
parser.add_argument('--list-topics', action='store_true', help='List all topics in the project')

project_id = os.getenv("GCP_PROJECT_ID")
service_account_file = os.getenv("GCP_SERVICE_ACCOUNT_FILE")

# print project and service account path
#print(f"Project ID: {project_id}")
# print(f"Service Account File: {service_account_file}")

args = parser.parse_args()

# check for arg create_topic
if args.create_topic:
    topic_name = args.create_topic

    print(f"Creating topic: {topic_name}")

    publisher = pubsub_v1.PublisherClient.from_service_account_file(service_account_file)
    topic_path = publisher.topic_path(project_id, topic_name)

    topic = publisher.create_topic(request={"name": topic_path})

    print(f"Created topic: {topic.name}")

# check for arg list_topics
elif args.list_topics:
    print("Listing all topics...")

    publisher = pubsub_v1.PublisherClient.from_service_account_file(service_account_file)
    project_path = f"projects/{project_id}"

    # List all topics in the project
    request = {"project": project_path}
    page_result = publisher.list_topics(request=request)

    topics = []
    for topic in page_result:
        topics.append(topic.name)

    if topics:
        print(f"Found {len(topics)} topic(s):")
        for topic in topics:
            print(f"  - {topic}")
    else:
        print("No topics found in the project.")

else:
    print("No action specified. Use --create-topic <topic_name> to create a topic or --list-topics to list all topics.")


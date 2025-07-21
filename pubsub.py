import os
from google.cloud import pubsub_v1
from dotenv import load_dotenv
import argparse
import time

os.environ.clear()
load_dotenv()

# Set up argument parser
parser = argparse.ArgumentParser(description='Argument parser for pubsub.')
parser.add_argument('--create-topic', type=str, help='Name of the topic to create')
parser.add_argument('--enable-ordering', action='store_true', help='Enable message ordering for topic (use with --create-topic)')
parser.add_argument('--list-topics', action='store_true', help='List all topics in the project')
parser.add_argument('--subscribe', nargs=2, metavar=('TOPIC_NAME', 'SUBSCRIPTION_NAME'), help='Create a subscription to a topic')
parser.add_argument('--ordered', action='store_true', help='Enable message ordering for subscription (use with --subscribe)')
parser.add_argument('--publish', nargs=2, metavar=('TOPIC_NAME', 'MESSAGE'), help='Publish a message to a topic')
parser.add_argument('--ordering-key', type=str, help='Ordering key for message ordering (use with --publish)')
parser.add_argument('--receive', nargs='+', metavar=('SUBSCRIPTION_NAME', 'MAX_MESSAGES'), help='Receive pending messages from a subscription (optional: specify max number of messages)')
parser.add_argument('--listen', nargs='+', metavar=('SUBSCRIPTION_NAME', 'TIMEOUT'), help='Listen for messages from a subscription (optional: specify timeout in seconds, default: 60 seconds)')

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

# check for arg subscribe
elif args.subscribe:
    topic_name, subscription_name = args.subscribe

    print(f"Creating subscription '{subscription_name}' to topic '{topic_name}'")
    if args.ordered:
        print("Message ordering enabled for this subscription")

    subscriber = pubsub_v1.SubscriberClient.from_service_account_file(service_account_file)
    topic_path = subscriber.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    # Create the subscription with optional message ordering
    subscription_request = {"name": subscription_path, "topic": topic_path}
    if args.ordered:
        subscription_request["enable_message_ordering"] = True

    subscription = subscriber.create_subscription(request=subscription_request)

    print(f"Created subscription: {subscription.name}")
    if args.ordered:
        print("✓ Message ordering is enabled for this subscription")

# check for arg publish
elif args.publish:
    topic_name, message = args.publish

    print(f"Publishing message to topic '{topic_name}': {message}")
    if args.ordering_key:
        print(f"Using ordering key: {args.ordering_key}")

    publisher = pubsub_v1.PublisherClient.from_service_account_file(service_account_file)
    topic_path = publisher.topic_path(project_id, topic_name)

        # Publish the message with optional ordering key
    if args.ordering_key:
        # Configure publisher options for message ordering
        publisher_options = pubsub_v1.types.PublisherOptions(
            enable_message_ordering=True
        )
        publisher = pubsub_v1.PublisherClient.from_service_account_file(
            service_account_file,
            publisher_options=publisher_options
        )

        # Publish with ordering key
        future = publisher.publish(topic_path, message.encode("utf-8"), ordering_key=args.ordering_key)
        message_id = future.result()
        print(f"Published message with ID: {message_id}")
        print(f"✓ Message published with ordering key: {args.ordering_key}")
    else:
        # Use regular publish for unordered messages
        future = publisher.publish(topic_path, message.encode("utf-8"))
        message_id = future.result()
        print(f"Published message with ID: {message_id}")

# check for arg receive (single message)
elif args.receive:
    subscription_name = args.receive[0]

    # Check if max_messages is provided
    if len(args.receive) > 1:
        try:
            max_messages = int(args.receive[1])
            if max_messages <= 0:
                print("Error: Max messages must be a positive number.")
                exit(1)
        except ValueError:
            print("Error: Max messages must be a valid number.")
            exit(1)
    else:
        max_messages = 1000  # Default to pull all (up to 1000)

    print(f"Receiving pending messages from subscription '{subscription_name}'...")
    if max_messages < 1000:
        print(f"Maximum messages to pull: {max_messages}")
    else:
        print("Pulling all pending messages (up to 1000)")

    subscriber = pubsub_v1.SubscriberClient.from_service_account_file(service_account_file)
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    # Pull messages based on max_messages parameter
    response = subscriber.pull(request={"subscription": subscription_path, "max_messages": max_messages})

    if response.received_messages:
        print(f"Found {len(response.received_messages)} pending message(s):")
        ack_ids = []

        for i, received_message in enumerate(response.received_messages, 1):
            message = received_message.message
            print(f"\nMessage {i}:")
            print(f"  Content: {message.data.decode('utf-8')}")
            print(f"  Message ID: {message.message_id}")
            print(f"  Publish time: {message.publish_time}")
            ack_ids.append(received_message.ack_id)

        # Acknowledge all messages
        subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": ack_ids})
        print(f"\nAll {len(response.received_messages)} message(s) acknowledged.")
    else:
        print("No pending messages available in the subscription.")

# check for arg listen (continuous listening)
elif args.listen:
    subscription_name = args.listen[0]

    # Check if timeout is provided
    if len(args.listen) > 1:
        try:
            timeout = int(args.listen[1])
            if timeout <= 0:
                print("Error: Timeout must be a positive number.")
                exit(1)
            print(f"Listening for messages from subscription '{subscription_name}' for {timeout} seconds...")
            print("Press Ctrl+C to stop early\n")
        except ValueError:
            print("Error: Timeout must be a valid number.")
            exit(1)
    else:
        timeout = None
        print(f"Listening indefinitely for messages from subscription '{subscription_name}'...")
        print("Press Ctrl+C to stop\n")

    subscriber = pubsub_v1.SubscriberClient.from_service_account_file(service_account_file)
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback(message):
        print(f"Received message: {message.data.decode('utf-8')}")
        print(f"Message ID: {message.message_id}")
        print(f"Publish time: {message.publish_time}")
        print("-" * 50)
        message.ack()

    # Start the subscriber
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        # Wait for the specified timeout or indefinitely
        if timeout:
            streaming_pull_future.result(timeout=timeout)
        else:
            streaming_pull_future.result()
    except Exception as e:
        if timeout and "timeout" in str(e).lower():
            print(f"\nTimeout reached ({timeout} seconds). Stopping message reception.")
        else:
            print(f"Error: {e}")
    finally:
        # Cancel the subscription
        streaming_pull_future.cancel()
        streaming_pull_future.result()

else:
    print("No action specified. Use --create-topic <topic_name> [--enable-ordering] to create a topic (with optional message ordering), --list-topics to list all topics, --subscribe <topic_name> <subscription_name> [--ordered] to create a subscription (with optional message ordering), --publish <topic_name> <message> [--ordering-key <key>] to publish a message (with optional ordering key), --receive <subscription_name> [max_messages] to receive pending messages, or --listen <subscription_name> [timeout] to listen for messages.")


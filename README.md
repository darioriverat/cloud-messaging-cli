# Cloud Messaging CLI

A command-line tool for managing cloud messaging services including Google Cloud Pub/Sub, with plans to support AWS SNS/SQS, Azure Service Bus, and other cloud messaging platforms.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cloud-messaging-cli
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
uv pip install -e .
```

## Configuration

The following environment variables are available and must be setup in order to
connect with the Pub/Sub service:

```
GCP_PROJECT_ID=your-project-id
GCP_SERVICE_ACCOUNT_PATH=path/to/your/service-account.json
```

### GCP

#### Creating a Service Account in GCP

1. Once you're logged into GCP, go to **IAM & Admin > Service Accounts**.
2. Click **“Create Service Account”**.
3. Enter a name for the service account and click **“Create and Continue”**.
4. In the **Permissions** step:
   -  Open the **Role** dropdown.
   - Select **“Pub/Sub Admin”**.
   - Click **“Continue”**, then **“Done”**.

#### Creating a Service Account Key (JSON):

1. After the service account is created, click the **three vertical dots** next to it and select **“Manage Keys”**.
2. Click **“Add Key”** and choose **“Create new key”**.
3. Select **JSON** as the key type and click **“Create”**.

The key file will be downloaded to your computer. Store it securely, as it contains credentials for accessing your GCP services.

## Usage

### Topic Management

**List all topics:**
```bash
python pubsub.py --list-topics
```

**Create a topic:**
```bash
python pubsub.py --create-topic mytopic
```

### Subscription Management

**Create a subscription to a topic:**
```bash
python pubsub.py --subscribe mytopic subscription-name
```

**Create a subscription with message ordering enabled:**
```bash
python pubsub.py --subscribe mytopic subscription-name --ordered
```

> **Note**: Message ordering ensures that messages with the same ordering key are delivered in the order they were published. This is useful for scenarios where message sequence matters (e.g., user actions, financial transactions).

### Message Publishing

**Publish a message to a topic:**
```bash
python pubsub.py --publish mytopic "Your message here"
```

**Publish a message with an ordering key:**
```bash
python pubsub.py --publish mytopic "Your message here" --ordering-key user-123
```

> **Note**: Ordering keys are used with ordered subscriptions to ensure messages with the same key are delivered in the order they were published. This is essential for maintaining message sequence for related events.

### Message Receiving

**Receive all pending messages from a subscription:**
```bash
python pubsub.py --receive subscription-name
```

**Receive a specific number of pending messages:**
```bash
python pubsub.py --receive subscription-name 5
```

**Receive just one message:**
```bash
python pubsub.py --receive subscription-name 1
```

### Message Listening

**Listen indefinitely for new messages:**
```bash
python pubsub.py --listen subscription-name
```

**Listen for a specific time period:**
```bash
python pubsub.py --listen subscription-name 30
```

**Listen for 2 minutes:**
```bash
python pubsub.py --listen subscription-name 120
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `--list-topics` | List all topics in the project | `python pubsub.py --list-topics` |
| `--create-topic <name>` | Create a new topic | `python pubsub.py --create-topic mytopic` |
| `--subscribe <topic> <subscription> [--ordered]` | Create a subscription to a topic (with optional message ordering) | `python pubsub.py --subscribe mytopic mysub --ordered` |
| `--publish <topic> <message> [--ordering-key <key>]` | Publish a message to a topic (with optional ordering key) | `python pubsub.py --publish mytopic "Hello" --ordering-key user-123` |
| `--receive <subscription> [count]` | Receive pending messages (optional count) | `python pubsub.py --receive mysub 5` |
| `--listen <subscription> [timeout]` | Listen for new messages (optional timeout in seconds) | `python pubsub.py --listen mysub 60` |

## Notes

- The `--receive` command processes all pending messages by default (up to 1000), or you can specify a maximum number
- The `--listen` command listens indefinitely by default, or you can specify a timeout in seconds
- All messages are automatically acknowledged after processing
- Use Ctrl+C to stop listening early
- Make sure your service account has the necessary Pub/Sub permissions
- Currently supports Google Cloud Pub/Sub, with plans to support other cloud messaging services

## Message Ordering

When you create a subscription with the `--ordered` flag, messages with the same ordering key will be delivered in the order they were published. This is particularly useful for:

- **Sequential Processing**: Events that must be processed in order (e.g., user actions, financial transactions)
- **State Management**: Scenarios where message order affects the final state
- **Data Consistency**: Ensuring data integrity when order matters

**Important Considerations:**
- Message ordering only works for messages with the same ordering key
- Ordered subscriptions have slightly reduced throughput compared to unordered subscriptions
- Existing subscriptions cannot be modified to enable ordering - you must create new ones
- When publishing messages to ordered subscriptions, consider using ordering keys for related messages
- Ordering keys should be consistent for related messages (e.g., use user ID for user actions, transaction ID for financial operations)
- The publisher automatically handles message ordering when ordering keys are provided

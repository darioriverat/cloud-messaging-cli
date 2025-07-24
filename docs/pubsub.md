# Google Cloud Pub/Sub CLI

A command-line tool for managing Google Cloud Pub/Sub topics, subscriptions, and messages as part of the GCP CLI Toolkit.

## Configuration

The following environment variables are required to connect with the Pub/Sub service:

```
GCP_PROJECT_ID=your-project-id
GCP_SERVICE_ACCOUNT_PATH=path/to/your/service-account.json
```

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

**Delete a topic:**
```bash
python pubsub.py --delete-topic mytopic
```

> **Important Note**: Deleting a topic will permanently remove it. However, subscriptions to the topic will remain and must be deleted separately. This action cannot be undone. Make sure you have backed up any important data before deletion.

### Subscription Management

**Create a subscription to a topic:**
```bash
python pubsub.py --subscribe mytopic subscription-name
```

**Create a subscription with message ordering enabled:**
```bash
python pubsub.py --subscribe mytopic subscription-name --ordered
```

**Delete a subscription:**
```bash
python pubsub.py --delete-subscription subscription-name
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
| `--delete-topic <name>` | Delete a topic | `python pubsub.py --delete-topic mytopic` |
| `--subscribe <topic> <subscription> [--ordered]` | Create a subscription to a topic (with optional message ordering) | `python pubsub.py --subscribe mytopic mysub --ordered` |
| `--delete-subscription <name>` | Delete a subscription | `python pubsub.py --delete-subscription mysub` |
| `--publish <topic> <message> [--ordering-key <key>]` | Publish a message to a topic (with optional ordering key) | `python pubsub.py --publish mytopic "Hello" --ordering-key user-123` |
| `--receive <subscription> [count]` | Receive pending messages (optional count) | `python pubsub.py --receive mysub 5` |
| `--listen <subscription> [timeout]` | Listen for new messages (optional timeout in seconds) | `python pubsub.py --listen mysub 60` |

## Notes

- The `--receive` command processes all pending messages by default (up to 1000), or you can specify a maximum number
- The `--listen` command listens indefinitely by default, or you can specify a timeout in seconds
- All messages are automatically acknowledged after processing
- Use Ctrl+C to stop listening early
- Make sure your service account has the necessary Pub/Sub permissions

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
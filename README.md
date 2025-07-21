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

4. Set up environment variables:
Create a `.env` file with your cloud provider credentials:
```
GCP_PROJECT_ID=your-project-id
GCP_SERVICE_ACCOUNT_FILE=path/to/your/service-account.json
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

### Subscription Management

**Create a subscription to a topic:**
```bash
python pubsub.py --subscribe mytopic subscription-name
```

### Message Publishing

**Publish a message to a topic:**
```bash
python pubsub.py --publish mytopic "Your message here"
```

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

## Examples

### Complete Workflow

1. **Create a topic:**
   ```bash
   python pubsub.py --create-topic notifications
   ```

2. **Create a subscription:**
   ```bash
   python pubsub.py --subscribe notifications email-subscription
   ```

3. **Publish a message:**
   ```bash
   python pubsub.py --publish notifications "Hello, this is a test message!"
   ```

4. **Receive pending messages:**
   ```bash
   python pubsub.py --receive email-subscription
   ```

5. **Listen for new messages:**
   ```bash
   python pubsub.py --listen email-subscription
   ```

### Testing Scenarios

**Process message backlog:**
```bash
python pubsub.py --receive email-subscription 10
```

**Monitor real-time messages:**
```bash
python pubsub.py --listen email-subscription 300
```

**Quick message check:**
```bash
python pubsub.py --receive email-subscription 1
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `--list-topics` | List all topics in the project | `python pubsub.py --list-topics` |
| `--create-topic <name>` | Create a new topic | `python pubsub.py --create-topic mytopic` |
| `--subscribe <topic> <subscription>` | Create a subscription to a topic | `python pubsub.py --subscribe mytopic mysub` |
| `--publish <topic> <message>` | Publish a message to a topic | `python pubsub.py --publish mytopic "Hello"` |
| `--receive <subscription> [count]` | Receive pending messages (optional count) | `python pubsub.py --receive mysub 5` |
| `--listen <subscription> [timeout]` | Listen for new messages (optional timeout in seconds) | `python pubsub.py --listen mysub 60` |

## Notes

- The `--receive` command processes all pending messages by default (up to 1000), or you can specify a maximum number
- The `--listen` command listens indefinitely by default, or you can specify a timeout in seconds
- All messages are automatically acknowledged after processing
- Use Ctrl+C to stop listening early
- Make sure your service account has the necessary Pub/Sub permissions
- Currently supports Google Cloud Pub/Sub, with plans to support other cloud messaging services
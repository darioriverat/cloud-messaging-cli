## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gcp_assistant
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

## Usage

Create a topic

```shell
python pubsub.py --create-topic mytopic
```

Create a subscription

```shell
python pubsub.py --subscribe mytopic subscription-name
```
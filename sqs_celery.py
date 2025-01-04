# Script you sent to me
from celery import Celery
from kombu import Exchange, Queue

app = Celery(
    'cel',
    broker='sqs://',
    backend='celery_s3.backends.S3Backend',
    broker_transport_options={
        'visibility_timeout': 3600,
        'task_create_missing_queues': False,
        'region': 'eu-central-1',
        'queue_name_prefix': 'cel-',
        'endpoint_url': 'https://sqs.eu-central-1.amazonaws.com'
    },
    broker_connection_retry_on_startup=True
)

# Define explicit queues
app.conf.task_queues = (
    Queue('queue1', Exchange('exchange1'), routing_key='route1'),
    Queue('queue2', Exchange('exchange2'), routing_key='route2'),
)

# Add S3 backend settings
app.conf.update(
    CELERY_S3_BACKEND_SETTINGS={
        'bucket': 'celery_back',
        'region': 'eu-central-1',
        'endpoint_url': 'https://s3.eu-central-1.amazonaws.com'
    }
)


@app.task
def add(x, y):
    return x + y


# Solution for BUG

# Initialize Celery app
app = Celery(
    'cel',
    broker='sqs://',
    backend='celery_s3.backends.S3Backend',
)

# Broker transport options
app.conf.broker_transport_options = {
    'visibility_timeout': 3600,  # Timeout for SQS messages
    'task_create_missing_queues': False,  # Prevent auto-creation of queues
    'region': 'eu-central-1',  # AWS region
    'queue_name_prefix': 'cel-',  # Prefix for queue names
    'endpoint_url': 'https://sqs.eu-central-1.amazonaws.com',  # Custom endpoint
}

# S3 Backend settings
app.conf.CELERY_S3_BACKEND_SETTINGS = {
    'bucket': 'celery_back',  # S3 bucket for backend
    'region': 'eu-central-1',  # AWS region
    'endpoint_url': 'https://s3.eu-central-1.amazonaws.com',  # Custom endpoint
}

# Define explicit queues
app.conf.task_queues = [
    Queue('queue1', Exchange('exchange1'), routing_key='route1'),
    Queue('queue2', Exchange('exchange2'), routing_key='route2'),
]

# Task routes (optional, for fine-grained control)
app.conf.task_routes = {
    'add': {'queue': 'queue1'},  # Example task to queue mapping
}

# Enable retry on broker connection startup
app.conf.broker_connection_retry_on_startup = True

# Define a sample task


@app.task
def add(x, y):
    return x + y
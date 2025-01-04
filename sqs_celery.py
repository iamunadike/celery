

# USE THIS FOR PASTEBIN https://pastebin.com/K2E7qRBk

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

# YOU CAN NOW USE THIS FOR PASTEBIN: https://pastebin.com/Nz9HZuAB

# Try executing with this code 
from celery_tasks import add

if __name__ == '__main__':
    try:
        # Asynchronously send the task to the specified queue
        result = add.apply_async(args=(10, 20), queue='queue1')
        print(f'Task ID: {result.id}')
        
        # Retrieve the result with a timeout
        task_result = result.get(timeout=60)
        print(f'Task result: {task_result}')
    except Exception as e:
        print(f"An error occurred while executing the task: {e}")


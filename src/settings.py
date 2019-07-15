"""Project settinsg."""

import os

ASSEMBLY_MQ_URL: str = (
    os.getenv('ASSEMBLY_MQ_URL') or 'amqp://guest:guest@127.0.0.1/'
)
ASSEMBLY_QUEUE_NAME: str = os.getenv('ASSEMBLY_QUEUE_NAME') or 'assembly'

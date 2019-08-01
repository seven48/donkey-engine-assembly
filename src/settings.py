"""Project settings."""

import os

ASSEMBLY_FTP_HOST: str = os.getenv('ASSEMBLY_FTP_HOST') or '127.0.0.1'
ASSEMBLY_FTP_PORT: int = int(os.getenv('ASSEMBLY_FTP_PORT') or '2121')

ASSEMBLY_MQ_URL: str = (
    os.getenv('ASSEMBLY_MQ_URL') or 'amqp://guest:guest@127.0.0.1/'
)
ASSEMBLY_QUEUE_NAME: str = os.getenv('ASSEMBLY_QUEUE_NAME') or 'assembly'
ASSEMBLY_MQ_MAX_MESSAGES: int = int(
    os.getenv('ASSEMBLY_MQ_MAX_MESSAGES') or '100',
)

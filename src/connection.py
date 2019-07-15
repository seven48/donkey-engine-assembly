"""Module for AMQL broker connection."""

from aio_pika import (
    Channel,
    Queue,
    RobustConnection,
    connect_robust,
    exceptions,
)

from src.task import Task


class Connection(object):
    """Connection to AMQP broker."""

    def __init__(self, url: str, queue_name: str):
        """Initialize connection credentials."""
        self.url = url
        self.queue_name = queue_name

        self.connection: RobustConnection = None
        self.channel: Channel = None
        self.queue: Queue = None

    async def connect(self):
        """Connect to AMQP."""
        self.connection = await connect_robust(
            url=self.url,
        )

        self.channel = await self.connection.channel()

        self.queue = await self.channel.declare_queue(
            self.queue_name,
            auto_delete=True,
        )

        return True

    async def close(self):
        """Close connection to AMQP."""
        await self.connection.close()

    async def get(self):
        """Get message from queue."""
        try:
            mq_message = await self.queue.get(timeout=5)
        except exceptions.QueueEmpty:
            return False
        else:
            return Task(mq_message)

    async def __aenter__(self):
        """Async enter to context operator."""
        return await self.connect()

    async def __aexit__(self, *_):
        """Async exit from context operator."""
        await self.close()

""" Module for AMQL broker connection """

from aio_pika import (
    connect_robust,
    RobustConnection,
    Channel,
    Queue,
    exceptions
)

from src.task import Task

class Connection:
    """ Class for initializing connection to AMQP broker """

    def __init__(self, url: str, queue_name: str):
        self.url = url
        self.queue_name = queue_name

        self.connection: RobustConnection = None
        self.channel: Channel = None
        self.queue: Queue = None

    async def connect(self):
        """ Connecting to AMQP """

        self.connection = await connect_robust(
            url=self.url
        )

        self.channel = await self.connection.channel()

        self.queue = await self.channel.declare_queue(
            self.queue_name,
            auto_delete=True
        )

        return True

    async def close(self):
        """ Close connection to AMQP """

        await self.connection.close()

    async def get(self):
        """ Get message from queue """

        try:
            result = await self.queue.get(timeout=5)
        except exceptions.QueueEmpty:
            return False
        else:
            return Task(result)

    async def __aenter__(self):
        result = await self.connect()
        return result

    async def __aexit__(self, *_):
        await self.close()

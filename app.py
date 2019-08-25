"""Main module of the application."""

from asyncio import get_event_loop

from src.connection import make_connection
from src.settings import (
    ASSEMBLY_MQ_MAX_MESSAGES,
    ASSEMBLY_MQ_URL,
    ASSEMBLY_QUEUE_NAME,
)
from src.task import Task


async def create_connection() -> None:
    """Create RabbitMQ connection.

    Make async RabbitMQ connection and
    bind callback for new messages in the queue.
    """
    return await make_connection(
        url=ASSEMBLY_MQ_URL,
        queue_name=ASSEMBLY_QUEUE_NAME,
        prefetch_count=ASSEMBLY_MQ_MAX_MESSAGES,
        callback=Task.recieve,
    )


if __name__ == '__main__':
    loop = get_event_loop()
    connection = loop.run_until_complete(create_connection())

    loop.run_forever()
    loop.run_until_complete(connection.close())

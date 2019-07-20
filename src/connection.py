"""Module for AMQL broker connection."""

from typing import Callable

from aio_pika import Channel, Connection, IncomingMessage, Queue, connect_robust

MessageReciever = Callable[[IncomingMessage], None]


async def make_connection(
    url: str,
    callback: MessageReciever,
    prefetch_count: int,
    queue_name: str,
) -> Connection:
    """Create connection to RabbitMQ."""
    connection: Connection = await connect_robust(url)

    channel: Channel = await connection.channel()

    await channel.set_qos(prefetch_count=prefetch_count)

    queue: Queue = await channel.declare_queue(
        queue_name,
        auto_delete=True,
    )

    await queue.consume(callback)

    return connection

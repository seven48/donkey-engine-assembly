"""Module for AMQL broker connection."""

from aio_pika import connect_robust


async def make_connection(url: str, callback, **kwargs):
    """Create connection to RabbitMQ."""
    connection = await connect_robust(url)

    channel = await connection.channel()

    await channel.set_qos(prefetch_count=kwargs['prefetch_count'])

    queue = await channel.declare_queue(
        kwargs['queue_name'],
        auto_delete=True,
    )

    await queue.consume(callback)

    return connection

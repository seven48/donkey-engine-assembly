"""Module for small functions for tests."""

from aio_pika import Message, connect_robust


async def publish(message):
    """Publush message to queue."""
    connection = await connect_robust(
        'amqp://guest:guest@127.0.0.1/',
    )

    channel = await connection.channel()

    await channel.default_exchange.publish(
        Message(message.encode()),
        routing_key='assembly',
    )

    await connection.close()

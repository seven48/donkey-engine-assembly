"""Main module of the application."""

from asyncio import get_event_loop

from src.connection import Connection
from src.settings import ASSEMBLY_MQ_URL, ASSEMBLY_QUEUE_NAME


async def main() -> None:
    """Run server."""
    connection = Connection(
        url=ASSEMBLY_MQ_URL,
        queue_name=ASSEMBLY_QUEUE_NAME,
    )
    async with connection:
        await connection.get()


if __name__ == '__main__':
    LOOP = get_event_loop()
    LOOP.run_until_complete(main())
    LOOP.close()

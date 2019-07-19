"""Module for testing Connection class."""

import pytest

from src.connection import make_connection
from src.settings import (
    ASSEMBLY_MQ_MAX_MESSAGES,
    ASSEMBLY_MQ_URL,
    ASSEMBLY_QUEUE_NAME,
)


@pytest.mark.asyncio
async def test_make_connection_success():
    """Test make_connection with success result."""
    connection = await make_connection(
        url=ASSEMBLY_MQ_URL,
        callback=None,
        prefetch_count=ASSEMBLY_MQ_MAX_MESSAGES,
        queue_name=ASSEMBLY_QUEUE_NAME,
    )
    assert connection
    await connection.close()

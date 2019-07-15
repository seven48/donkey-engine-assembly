"""Module for testing Connection class."""

import pytest
from aiormq.exceptions import ProbableAuthenticationError

from src.connection import Connection
from src.task import Task
from tests.routines import publish

SUCCESS_URL = 'amqp://guest:guest@127.0.0.1/'
WRONG_AUTH_URL = 'amqp://wrong:wrong@127.0.0.1/'
BAD_HOST_URL = 'amqp://user:pass@255.255.255.255/'
BAD_URL = 'bad url'
QUEUE_NAME = 'assembly'


@pytest.mark.asyncio
async def test_init():
    """Test regular successful connection."""
    connection = Connection(
        url=SUCCESS_URL,
        queue_name=QUEUE_NAME,
    )
    status = await connection.connect()
    assert isinstance(status, bool)
    assert status
    await connection.close()


@pytest.mark.asyncio
async def test_bad_auth():
    """Test bad auth credentials in url."""
    connection = Connection(
        url=WRONG_AUTH_URL,
        queue_name=QUEUE_NAME,
    )
    with pytest.raises(ProbableAuthenticationError):
        await connection.connect()


@pytest.mark.asyncio
async def test_bad_host():
    """Test bad host url."""
    connection = Connection(
        url=BAD_HOST_URL,
        queue_name=QUEUE_NAME,
    )
    with pytest.raises(ConnectionError):
        await connection.connect()


@pytest.mark.asyncio
async def test_bad_url():
    """Test random string instead of url."""
    connection = Connection(
        url=BAD_URL,
        queue_name=QUEUE_NAME,
    )
    with pytest.raises(ValueError):
        await connection.connect()


@pytest.mark.asyncio
async def test_async_context_manager():
    """Test "async with" context manager."""
    connection = Connection(
        url=SUCCESS_URL,
        queue_name=QUEUE_NAME,
    )
    async with connection as connection_result:
        assert isinstance(connection_result, bool)
        assert connection_result


@pytest.mark.asyncio
async def test_sync_context_manager():
    """Test not working sync with context manager."""
    connection = Connection(
        url=SUCCESS_URL,
        queue_name=QUEUE_NAME,
    )
    with pytest.raises(AttributeError):
        with connection:  # noqa: Z328
            pass  # noqa: Z420


@pytest.mark.asyncio
async def test_recieve_message():
    """Test receive regular message from queue."""
    connection = Connection(
        url=SUCCESS_URL,
        queue_name=QUEUE_NAME,
    )
    await connection.connect()

    await publish('Hello world!')

    message = await connection.get()
    assert isinstance(message, Task)
    assert message.text == 'Hello world!'

    await connection.close()

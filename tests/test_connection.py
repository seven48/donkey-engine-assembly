""" Module for testing Connection class """

import pytest

from aiormq.exceptions import ProbableAuthenticationError

from src.connection import Connection


SUCCESS_URL = 'amqp://guest:guest@127.0.0.1/'
WRONG_AUTH_URL = 'amqp://wrong:wrong@127.0.0.1/'
BAD_HOST_URL = 'amqp://user:pass@255.255.255.255/'
BAD_URL = 'bad url'
QUEUE_NAME = 'test_queue'


@pytest.mark.asyncio
async def test_init():
    """ Test regular successful connection """

    connection = Connection(
        url=SUCCESS_URL,
        queue_name=QUEUE_NAME
    )
    status = await connection.connect()
    assert isinstance(status, bool)
    assert status
    await connection.close()

@pytest.mark.asyncio
async def test_bad_auth():
    """ Test bad auth credentials in url """

    connection = Connection(
        url=WRONG_AUTH_URL,
        queue_name=QUEUE_NAME
    )
    with pytest.raises(ProbableAuthenticationError):
        await connection.connect()

@pytest.mark.asyncio
async def test_bad_host():
    """ Test bad host url """

    connection = Connection(
        url=BAD_HOST_URL,
        queue_name=QUEUE_NAME
    )
    with pytest.raises(ConnectionError):
        await connection.connect()

@pytest.mark.asyncio
async def test_bad_url():
    """ Test random string instead of url """

    connection = Connection(
        url=BAD_URL,
        queue_name=QUEUE_NAME
    )
    with pytest.raises(ValueError):
        await connection.connect()

@pytest.mark.asyncio
async def test_async_context_manager():
    """ Test "async with" context manager """

    connection = Connection(
        url=SUCCESS_URL,
        queue_name=QUEUE_NAME
    )
    async with connection as result:
        assert isinstance(result, bool)
        assert result

@pytest.mark.asyncio
async def test_sync_context_manager():
    """ Test not working sync with context manager """

    connection = Connection(
        url=SUCCESS_URL,
        queue_name=QUEUE_NAME
    )
    with pytest.raises(AttributeError):
        with connection:  # pylint: disable=not-context-manager
            pass

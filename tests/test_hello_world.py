""" Module for hello world testing (just for initiating) """

import pytest


@pytest.mark.asyncio
async def test_test():
    """ Test Hello world """

    assert 2 + 2 == 4

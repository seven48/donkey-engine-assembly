"""Module for testing Task."""

from json import dumps

import pytest

from src.assets import workers
from src.task import Task

success_message_body = {
    'game': 'Minecraft: Java Edition',
    'version': '1.2.5',
    'mods': [
        'CraftBukkit',
    ],
    'configs': {
        'max-players': 20,
    },
}


class MockIncommingMessage(object):
    """Mock class of pika IncommingMessage."""

    def __init__(self, text):
        """Initializate mock object."""
        self.body = dumps(text).encode()


@pytest.mark.asyncio
async def test_task_success():
    """Test Task class with success result."""
    message = MockIncommingMessage(success_message_body)

    task = Task(message)
    assert task.text == message.body.decode('UTF-8')
    assert task.json == success_message_body

    worker = task.delegate()
    minecraft_builder = workers.get('Minecraft: Java Edition')
    assert isinstance(worker, minecraft_builder)

    assert task.json['game'] == worker.game
    assert task.json['version'] == worker.version

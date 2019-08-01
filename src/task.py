"""Module for class Task."""

from json import loads

from src.assets import workers


class Task(object):
    """Task delegating."""

    def __init__(self, message):
        """Task init method."""
        self.text = message.body.decode('UTF-8')
        self.json = loads(self.text)

    def delegate(self):
        """Get the necessary builder and create worker."""
        game_name = self.json['game']

        builder = workers.get(game_name)
        if builder:
            return builder(self.json)

    @classmethod
    async def recieve(cls, message):
        """Recieve message from mq."""
        async with message.process():
            task_handler = cls(message)
            worker = task_handler.delegate()
            await worker.build()

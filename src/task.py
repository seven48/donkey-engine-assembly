"""Module for delegating tasks that are received from RabbitMQ queue."""

from json import loads

from src.assets import workers


class Task(object):
    """Delegate and run a task which is taken from RabbitMQ queue."""

    def __init__(self, message):
        """Parse RabbitMQ message and save it to class attribute."""
        self.text = message.body.decode('UTF-8')
        self.json = loads(self.text)

    def delegate(self):
        """Get necessary server builder.

        Get the game server builder from `assets`
        by name and make an instance of it.
        """
        game_name = self.json['game']

        builder = workers.get(game_name)
        if builder:
            return builder(self.json)

    @classmethod
    async def recieve(cls, message):
        """Process RabbitMQ message.

        Receive a message from RabbitMQ, parse it, get the specific builder for
        this task, set it up and run.
        This method is bound as an async RabbitMQ message callback.
        """
        async with message.process():
            task_handler = cls(message)
            worker = task_handler.delegate()
            await worker.build()

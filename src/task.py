"""Module for class Task."""


class Task(object):
    """Task delegating."""

    def __init__(self, message):
        """Mock init method."""
        self.text = message.body.decode('UTF-8')

""" Module for class Task """

class Task:  # pylint: disable=too-few-public-methods
    """ Class for task delegating """

    def __init__(self, message):
        self.text = message.body.decode('UTF-8')

"""Module for building server objects."""


class MinecraftBuilder(object):
    """Minecraft: Java Edition server building."""

    def __init__(self, options):
        """Initializate builder with specified options."""
        self.version = options['version']
        self.mods = options['mods']
        self.configs = options['configs']

    def build(self):
        """Build minecraft server."""

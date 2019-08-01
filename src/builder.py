"""Module for building server objects."""

from io import BytesIO

from aioftp import ClientSession

from src.settings import ASSEMBLY_FTP_HOST, ASSEMBLY_FTP_PORT


class MinecraftBuilder(object):
    """Minecraft: Java Edition server building."""

    def __init__(self, options):
        """Initializate builder with specified options."""
        self.game = options['game']
        self.version = options['version']

        self.storage = BytesIO()

    async def prepare_server(self):
        """Init pure server instance and save it to `self.storage`."""
        client_session = ClientSession(
            host=ASSEMBLY_FTP_HOST,
            port=ASSEMBLY_FTP_PORT,
        )

        async with client_session as client:
            ftp_path = '/games/{0}/{1}/server.jar'.format(
                self.game,
                self.version,
            )
            async with client.download_stream(ftp_path) as stream:
                async for block in stream.iter_by_block():
                    self.storage.write(block)

    async def build(self):
        """Build minecraft server."""
        await self.prepare_server()

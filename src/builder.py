"""Module for building game servers and saving them to FTP."""

from io import BytesIO

from aioftp import ClientSession

from src.settings import ASSEMBLY_FTP_HOST, ASSEMBLY_FTP_PORT


class MinecraftBuilder(object):
    """Minecraft: Java Edition server building."""

    def __init__(self, options):
        """Initialize a Minecraft server builder.

        Parse incomming options. Get build id, game name and game version data.
        """
        self.build_id = options['build']['id']
        self.game = options['game']
        self.version = options['version']

        self.storage = BytesIO()

    async def prepare_server(self):
        """Init Minecraft server.

        Download pure Minecraft server without any mods and settings from FTP
        and save it to `self.storage` class attribute to work with it to:
        - save mods into it
        - update settings.
        """
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
                self.storage.seek(0)

    async def stor_server(self):
        """Upload local Minecraft server instance to FTP.

        Upload prepared Minecraft server instance from `self.storage` attribute
        to Donkey Engine FTP server to special directory.
        """
        client_session = ClientSession(
            host=ASSEMBLY_FTP_HOST,
            port=ASSEMBLY_FTP_PORT,
        )
        async with client_session as client:
            server_directory = '/servers/{0}'.format(self.build_id)
            await client.make_directory(server_directory)
            full_path = '/servers/{0}/server.jar'.format(self.build_id)
            async with client.upload_stream(full_path) as stream:
                await stream.write(self.storage.read())

    async def build(self):
        """Minecraft server build pipeline.

        This method will be called from lowest-level module `Task`
        in method `Task.recieve(cls, message)`.
        This method creates a Minecraft server by calling helper methods.

        Algorithm in method deals with the following tasks:
        - download server from FTP
        - upload prepared Minecraft server to FTP.
        """
        await self.prepare_server()
        await self.stor_server()

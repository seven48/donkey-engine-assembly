"""Module for building game servers and saving them to FTP."""

from io import BytesIO, StringIO

from aioftp import ClientSession

from src.settings import ASSEMBLY_FTP_HOST, ASSEMBLY_FTP_PORT

properties_default_values = {
    'generator-settings': None,
    'op-permission-level': 4,
    'allow-nether': True,
    'level-name': 'Map',
    'enable-query': False,
    'allow-flight': False,
    'announce-player-achievements': True,
    'server-port': 25565,
    'max-world-size': 29999984,
    'level-type': 'DEFAULT',
    'enable-rcon': False,
    'force-gamemode': False,
    'level-seed': None,
    'server-ip': None,
    'network-compression-threshold': 256,
    'max-build-height': 256,
    'spawn-npcs': True,
    'white-list': False,
    'spawn-animals': True,
    'snooper-enabled': True,
    'hardcore': False,
    'resource-pack-sha1': None,
    'online-mode': True,
    'resource-pack': None,
    'pvp': True,
    'broadcast-console-to-ops': True,
    'difficulty': 1,
    'enable-command-block': False,
    'player-idle-timeout': 0,
    'gamemode': 0,
    'max-players': 20,
    'max-tick-time': 60000,
    'spawn-monsters': True,
    'view-distance': 10,
    'generate-structures': True,
    'motd': 'A Donkey Engine Minecraft server',
}


def convert_properties_value(conf_value):
    """Convert properties value.

    Builder class works with python build-in types but
    Minecraft server.properties file are read by Java application.
    There are some difference between python "True" and necessary value "true".
    """
    if isinstance(conf_value, str):
        return conf_value
    if isinstance(conf_value, bool):
        if conf_value:
            return 'true'
        return 'else'
    if conf_value is None:
        return ''
    return str(conf_value)


def convert_file_content(file_content):
    """Convert file content to bytes."""
    if isinstance(file_content, str):
        return bytes(file_content, 'UTF-8')
    return file_content


class MinecraftBuilder(object):
    """Minecraft: Java Edition server building."""

    def __init__(self, options):
        """Initialize a Minecraft server builder.

        Parse incomming options. Get build id, game name and game version data.
        """
        self.build_id = options['build']['id']
        self.game = options['game']
        self.configs = options['configs']
        self.version = options['version']

        self.files = {
            'server.jar': BytesIO(),
            'server.properties': StringIO(),
            'Dockerfile': StringIO(),
        }

    async def prepare_server(self):
        """Init Minecraft server.

        Download pure Minecraft server without any mods and settings from FTP
        and save it to storage class attribute to work with it to:
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
                    self.files['server.jar'].write(block)
                self.files['server.jar'].seek(0)

    def configure(self):
        """Configure server properties file.

        Accepts JSON data from RabbitMQ, convert it to Minecraft necessary value
        and store it to class atribute `self.server_properties`.
        """
        configured_properties = []

        for conf_key in properties_default_values:
            user_value = self.configs.get(conf_key)
            default_value = properties_default_values.get(conf_key)

            configured_properties.append(
                '{0}={1}\n'.format(
                    conf_key,
                    convert_properties_value(
                        user_value or default_value,
                    ),
                ),
            )

        self.files['server.properties'].writelines(configured_properties)
        self.files['server.properties'].seek(0)

    def generate_dockerfile(self):
        """Generate Dockerfile for hosting service.

        Creates Dockerfile for Minecraft Server file (server.jar)
        and properties file.
        """
        dockerfile_text = [
            'FROM openjdk:8u212-jre-alpine',
            'COPY ./server.jar /home/app/server.jar',
            'COPY ./server.properties ./home/app/server.properties',
            'WORKDIR /home/app/',
            'CMD ["java","-Xmx1024M","-Xms1024M","-jar","server.jar","nogui"]',
        ]
        self.files['Dockerfile'].write('\n'.join(dockerfile_text))
        self.files['Dockerfile'].seek(0)

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
            await client.make_directory('/servers/{0}'.format(self.build_id))

            for filename in self.files:
                full_path = '/servers/{0}/{1}'.format(
                    self.build_id,
                    filename,
                )
                async with client.upload_stream(full_path) as stream:
                    await stream.write(
                        convert_file_content(self.files[filename].read()),
                    )

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
        self.configure()
        self.generate_dockerfile()
        await self.stor_server()

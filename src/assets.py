"""Project assets.

These assets help to delegate a task for a specific minecraft server builder.
"""

from src.builder import MinecraftBuilder

workers = {
    'Minecraft: Java Edition': MinecraftBuilder,
}

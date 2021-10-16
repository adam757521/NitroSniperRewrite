import discord
from discord.ext import commands
from typing import Optional


class StatusConverter(commands.Converter):
    """
    Represents a converter that converts str to a status
    """

    async def convert(self, ctx, argument: str) -> Optional[discord.Status]:
        try:
            return discord.Status(argument)
        except ValueError:
            raise commands.BadArgument(f"Status '{argument}' is invalid.")

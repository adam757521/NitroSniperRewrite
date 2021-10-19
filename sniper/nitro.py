from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from .core import SniperBot
    from selfbotUtils.nitro import NitroResponse
    import discord

__all__ = ("CustomNitroResponse",)


@dataclass
class CustomNitroResponse:
    """
    Represents a CustomNitroResponse.
    """

    response: NitroResponse
    message: discord.Message
    request_time: float
    receiver: discord.User
    redeemer: SniperBot

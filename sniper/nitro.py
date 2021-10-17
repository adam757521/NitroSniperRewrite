from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import SniperBot
    from selfbotUtils.nitro import NitroResponse
    import discord

__all__ = ("CustomNitroResponse",)


class CustomNitroResponse:
    """
    Represents a CustomNitroResponse.
    """

    __slots__ = ("response", "message", "request_time", "receiver", "redeemer")

    def __init__(
        self,
        response: NitroResponse,
        message: discord.Message,
        request_time: float,
        receiver: discord.User,
        redeemer: SniperBot,
    ) -> None:
        self.response = response
        self.message = message
        self.request_time = request_time
        self.receiver = receiver
        self.redeemer = redeemer

    def __str__(self):
        return f"<{self.__class__.__name__} response={self.response}>"

    def __repr__(self):
        return f"<{self.__class__.__name__} response={self.response}, message={self.message}, receiver={self.receiver}>"

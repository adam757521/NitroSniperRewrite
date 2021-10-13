from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selfbotUtils.nitro import NitroResponse
    import discord

__all__ = ("CustomNitroResponse",)


class CustomNitroResponse:
    """
    Represents a CustomNitroResponse.
    """

    __slots__ = ("server_response", "message", "request_time")

    def __init__(
        self,
        server_response: NitroResponse,
        message: discord.Message,
        request_time: float,
    ) -> None:
        self.server_response = server_response
        self.message = message
        self.request_time = request_time

    def __str__(self):
        return f"<{self.__class__.__name__} server_response={self.server_response}>"

    def __repr__(self):
        return f"<{self.__class__.__name__} server_response={self.server_response}, message={self.message}>"

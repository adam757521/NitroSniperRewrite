from __future__ import annotations

import asyncio
import logging
import os
import re
import sys
import time
from typing import List, Dict, Optional

import aiohttp
import discord
import pathlib
import selfbotUtils
from selfbotUtils import NitroServerResponse

from .constants import Delay, Webhook
from discord.ext import commands

from .nitro import CustomNitroResponse

__all__ = ("SniperBot", "MainSniperBot")


class SniperBot(commands.Bot):
    """
    Represents an alt sniper bot that redeems code on the main bot.
    """

    __slots__ = ("main", "token")

    LINKS = ("discord.gift", "discordapp.com/gifts", "discord.com/gifts")
    GIFT_RE = re.compile(fr'({"|".join(LINKS)})/\w{{16,24}}')

    def __init__(self, token: str, main: MainSniperBot):
        super().__init__("<<<", help_command=None, self_bot=True)

        self.main = main
        self.token = token

    def find_codes(self, text: str) -> List[str]:
        """
        Finds and returns the discord gift codes in the text.

        :param str text: The text.
        :return: The list of codes.
        :rtype: List[str]
        """

        codes = []

        for match in self.GIFT_RE.finditer(text):
            current_code = match.group(0)

            for link in self.LINKS:
                current_code = current_code.replace(link + "/", "")

            codes.append(current_code)

        return codes

    async def on_ready(self):
        print(f"{self.user} is ready.")

    @staticmethod
    async def send_webhook_alert(response: CustomNitroResponse) -> None:
        """
        |coro|

        Sends embed information about the response to the webhook.

        :param CustomNitroResponse response: The nitro response.
        :return: None
        :rtype: None
        """

        webhook_url = Webhook.URL

        if webhook_url:
            response_filter = Webhook.FILTER
            if (
                response_filter
                and response.response.server_response not in response_filter
            ):
                return

            embed = discord.Embed(title="Nitro Alert", color=0x00FF00)

            embed.add_field(
                name="Server Response",
                value=str(response.response.server_response),
                inline=False,
            )

            embed.add_field(
                name="Author", value=str(response.message.author), inline=False
            )

            embed.add_field(
                name="Guild",
                value=response.message.guild and response.message.guild.name,
                inline=False,
            )

            embed.add_field(name="Receiver", value=str(response.receiver), inline=False)

            embed.add_field(
                name="Response Time",
                value=f"{round(response.request_time * 1000)}ms",
                inline=False,
            )

            if response.response.server_response == NitroServerResponse.CLAIMED:
                embed.add_field(
                    name="Nitro Type", value=response.response.nitro_type, inline=False
                )

            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(
                    webhook_url, adapter=discord.AsyncWebhookAdapter(session)
                )
                await webhook.send(embed=embed)

    async def on_message(self, message):
        codes = self.find_codes(
            message.content
        )  # Make sure you use discord.py-self to access the message content.

        if not codes:
            await self.process_commands(message)
            return

        for code in codes:
            if (
                code not in self.main.cache
            ):  # Code is not already cached (tried to redeem).
                self.main.cache[code] = None
                # The code will not be in the cache until the API responds, meaning the code will remain not recognized
                # and might be handled as an not cached code and be redeemed multiple times while waiting for the API
                # response.

                await asyncio.sleep(
                    Delay.DM_DELAY if not message.guild else Delay.SERVER_DELAY
                )

                start = time.time()
                code_response = await self.main.self_bot_utils.redeem_gift(code)

                custom_response = CustomNitroResponse(
                    code_response, message, time.time() - start, self.user
                )
                self.main.cache[code] = custom_response

                if (
                    custom_response.response.server_response
                    == NitroServerResponse.UNKNOWN
                ):
                    print(NitroServerResponse.response.raw)

                print(custom_response, message.author, code)
                await self.send_webhook_alert(custom_response)

    async def start_bot(self) -> None:
        """
        |coro|

        Runs the bot with the bot token.

        :return: None
        :rtype: None
        """

        try:
            await super().start(self.token)
        except discord.LoginFailure:
            print(f"Token '{self.token}' is invalid.")
            await self.main.self_bot_utils.close()
            sys.exit(1)


class MainSniperBot(SniperBot):
    """
    Represents a main sniper bot.
    """

    __slots__ = (
        "cache",
        "alts",
        "self_bot_utils",  # The selfbotUtils client that redeems codes.
    )

    def __init__(self, token: str) -> None:
        super().__init__(token, self)
        self.load_cogs()

        self.alts: List[SniperBot] = []
        self.cache: Dict[str, Optional[CustomNitroResponse]] = {}
        self.self_bot_utils = selfbotUtils.Client(token, state=self._connection)

    def load_cogs(self) -> None:
        """
        Loads all the cogs in the directory.

        :return: None
        :rtype: None
        """

        path = str(pathlib.Path(__file__).parent.resolve())
        slash = "/" if "/" in path else "\\"
        for file in os.listdir(path + f"{slash}cogs"):
            if not file.endswith(".py") or file.startswith("__"):
                continue

            try:
                self.load_extension(f'sniper.cogs.{file.replace(".py", "")}')
                logging.info(f"Loaded cog {file}")
            except Exception as e:
                logging.critical(
                    f"An exception has been raised when loading cog {file}"
                )
                raise e

    def create_alts(self, tokens: List[str]) -> List[SniperBot]:
        """
        Creates alts for the main bot.

        :param List[SniperBot] tokens: The tokens.
        :return: The created alts.
        :rtype: List[SniperBot]
        """

        alts = [SniperBot(token, self) for token in tokens]
        self.alts = alts

        return alts

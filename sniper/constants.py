import discord
from selfbotUtils.enums import NitroServerResponse

from .enums import StatusType


class Accounts:
    MAIN_TOKEN = ""
    ALTS = []
    AUTOMATIC_STATUS_TYPE = (
        StatusType.ALL
    )  # Can be ALL, ALTS and MAIN. Can also be None to disable this feature.
    AUTOMATIC_STATUS = discord.Status.offline


class Delay:
    DM_DELAY = 0
    SERVER_DELAY = 0


class Webhook:
    URL = ""
    FILTER = [
        NitroServerResponse.CLAIMED
    ]  # Can be an empty list for all, when using heroku, please set this to 6 for claimed.

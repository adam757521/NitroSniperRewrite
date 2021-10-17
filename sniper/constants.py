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
    AFK = True


class Delay:
    DM_DELAY = 0
    SERVER_DELAY = 0


class Cooldown:
    NITRO_COOLDOWN = 2  # Can be None if you want to ignore cooldowns.
    NITRO_COOLDOWN_HOURS = 24
    REDEEM_ON_ALT = True


class Webhook:
    URL = ""
    FILTER = [
        NitroServerResponse.CLAIMED
    ]  # Can be an empty list for all, when using heroku, please set this to 6 for claimed.

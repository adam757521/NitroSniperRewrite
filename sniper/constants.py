from selfbotUtils.enums import NitroServerResponse


class Accounts:
    MAIN_TOKEN = ""
    ALTS = []


class Delay:
    DM_DELAY = 0
    SERVER_DELAY = 0


class Webhook:
    URL = ""
    FILTER = [
        NitroServerResponse.CLAIMED
    ]  # Can be an empty list for all, when using heroku, please set this to 6 for claimed.

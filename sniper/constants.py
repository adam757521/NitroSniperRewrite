from selfbotUtils.enums import NitroServerResponse


class Accounts:
    MAIN_TOKEN = "mfa.tnomybWcwaE6kALcMsb8YlwYXOw4wbV80R6mv7t14oHR755zPNGz6iZAeKgGURdS71JQsNPNWkMekUYn02Xj"
    ALTS = []


class Delay:
    DM_DELAY = 0
    SERVER_DELAY = 0


class Webhook:
    URL = ""
    FILTER = [
        NitroServerResponse.CLAIMED
    ]  # Can be an empty list for all, when using heroku, please set this to 6 for claimed.

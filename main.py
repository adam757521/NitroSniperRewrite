import asyncio

import constants
from sniper import MainSniperBot


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    main_account = MainSniperBot(constants.Accounts.MAIN_TOKEN)
    main_account.create_alts(constants.Accounts.ALTS)

    loop.create_task(main_account.start_bot())

    for alt in main_account.alts:
        loop.create_task(alt.start_bot())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

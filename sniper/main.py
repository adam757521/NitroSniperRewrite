import asyncio
import logging

from core.heroku import overwrite_heroku_values
import sniper.constants
from core.core import MainSniperBot

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.CRITICAL)

    overwrite_heroku_values()
    # Adds heroku support to the program, overwrites the values in constants.py with heroku configuration.

    loop = asyncio.get_event_loop()

    main_account = MainSniperBot(sniper.constants.Accounts.MAIN_TOKEN)
    main_account.create_alts(sniper.constants.Accounts.ALTS)

    loop.create_task(main_account.start_bot())

    for alt in main_account.alts:
        loop.create_task(alt.start_bot())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

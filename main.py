import asyncio
import logging

import sniper

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.CRITICAL)

    sniper.overwrite_heroku_values()
    # Adds heroku support to the program, overwrites the values in constants.py with heroku configuration.

    loop = asyncio.get_event_loop()

    main_account = sniper.MainSniperBot(sniper.Accounts.MAIN_TOKEN)
    main_account.create_alts(sniper.Accounts.ALTS)

    loop.create_task(main_account.start_bot())

    for alt in main_account.alts:
        loop.create_task(alt.start_bot())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

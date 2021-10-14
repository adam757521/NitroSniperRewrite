import json
import os

import constants


class InvalidHerokuConfiguration(Exception):
    """
    Raised when invalid heroku configuration is passed.
    """


def get_class_config_attributes(class_config):
    return [
        attr
        for attr in dir(class_config)
        if not callable(getattr(class_config, attr)) and not attr.startswith("__")
    ]


def overwrite_heroku_values():
    if "settings" not in os.environ:
        return

    try:
        user_config = json.loads(os.environ["settings"])
    except json.decoder.JSONDecodeError:
        raise InvalidHerokuConfiguration(
            "Settings variable does not contain valid JSON."
        )

    config_classes = [constants.Accounts, constants.Delay, constants.Webhook]

    for config_class in config_classes:
        class_name = config_class.__name__
        config_category = user_config.get(class_name)

        if config_category is None:
            raise InvalidHerokuConfiguration(
                f"Heroku settings variables does not have '{class_name}' category."
            )

        for attr in get_class_config_attributes(config_class):
            config_value = config_category.get(attr)

            if config_value is None:
                raise InvalidHerokuConfiguration(
                    f"Heroku settings variable does not have a '{attr}' key in '{class_name}'"
                )

            setattr(config_class, attr, config_value)

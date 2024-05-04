# logging_config.py
import logging
import logging.config


def configure_logging():
    if logging.getLogger().handlers:
        # The Lambda environment pre-configures a handler logging to stderr.
        # If a handler is already configured, .basicConfig does not execute.
        # Thus we set the level directly.
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO)
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console"],
                "level": "INFO",
            },
        },
    }

    logging.config.dictConfig(logging_config)

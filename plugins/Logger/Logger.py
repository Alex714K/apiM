import logging
import logging.config


def activate_loggers():
    dictLogConfig = {
        "version": 1,
        "handlers": {
            "fileHandler": {
                "class": "logging.FileHandler",
                "formatter": "myFormatter",
                "filename": "data/logs/logs.log",
                "level": "INFO",
                "encoding": "UTF-8"
            },
            "rootHandler": {
                "class": "logging.FileHandler",
                "formatter": "myFormatter",
                "filename": "data/logs/all_trash.log",
                "level": "DEBUG",
                "encoding": "UTF-8"
            },
            "consoleHandler": {
                "class": "logging.StreamHandler",
                "formatter": "myFormatter",
                "level": "INFO"
            }
        },
        "loggers": {
            "root": {
                "handlers": ["rootHandler"],
                "level": "DEBUG",
            },
            "extraInfo": {
                "handlers": ["fileHandler", "consoleHandler"],
                "level": "INFO",
            },
            "RequestWB": {
                "handlers": ["fileHandler"],
                "level": "DEBUG"
            },
            "RequestOzon": {
                "handlers": ["fileHandler"],
                "level": "DEBUG"
            },
            "ApiWB": {
                "handlers": ["fileHandler"],
                "level": "DEBUG"
            },
            "ApiOzon": {
                "handlers": ["fileHandler"],
                "level": "DEBUG"
            }
        },
        "formatters": {
            "myFormatter": {
                "format": "%(levelname)s -> %(asctime)s: %(name)s - %(message)s"
            }
        }
    }
    logging.config.dictConfig(dictLogConfig)

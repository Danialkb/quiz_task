import sys

LOG_LEVEL = "DEBUG"

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
        },
        "uvicorn": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s [%(asctime)s] %(message)s",
            "use_colors": True,
        },
    },
    "handlers": {
        "default": {
            "level": LOG_LEVEL,
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
        "uvicorn": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "uvicorn",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
        },
        "uvicorn": {
            "handlers": ["uvicorn"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.error": {
            "level": LOG_LEVEL,
            "handlers": ["uvicorn"],
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["uvicorn"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

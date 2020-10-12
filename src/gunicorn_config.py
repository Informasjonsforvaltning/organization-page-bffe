from dotenv import load_dotenv
from os import environ as env
import logging
from gunicorn import glogging
import multiprocessing

load_dotenv()

PORT = env.get("HOST_PORT", "8080")
DEBUG_MODE = env.get("DEBUG_MODE", False)
LOG_LEVEL = env.get("LOG_LEVEL", "info")

# Gunicorn config
bind = ":" + PORT
workers = 1
threads = 1
loglevel = str(LOG_LEVEL)
accesslog = '-'

# Need to override the logger to remove healthcheck (ping) form accesslog


class CustomGunicornLogger(glogging.Logger):

    def setup(self, cfg):
        super().setup(cfg)

        # Add filters to Gunicorn logger
        logger = logging.getLogger("gunicorn.access")
        logger.addFilter(PingFilter())
        logger.addFilter(ReadyFilter())


class PingFilter(logging.Filter):
    def filter(self, record):
        return 'GET /ping' not in record.getMessage()


class ReadyFilter(logging.Filter):
    def filter(self, record):
        return 'GET /ready' not in record.getMessage()


logger_class = CustomGunicornLogger
import sys

from loguru import logger

# all times in UTC
logger.configure(
    handlers=[
        dict(
            sink=sys.stdout,
            format="{message}",
        ),
    ],
)

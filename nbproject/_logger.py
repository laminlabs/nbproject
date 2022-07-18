import sys

from loguru import logger

default_handler = dict(
    sink=sys.stdout,
    format="{level.icon} {message}",
)

logger.configure(handlers=[default_handler])
logger.level("WARNING", icon="🔶")

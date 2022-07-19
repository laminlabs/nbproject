import sys

from loguru import logger

default_handler = dict(
    sink=sys.stdout,
    format="{level.icon} {message}",
)

logger.configure(handlers=[default_handler])
logger.level("SUCCESS", icon="✅")
logger.level("WARNING", icon="🔶")

# ANSI color code: https://gist.github.com/iansan5653/c4a0b9f5c30d74258c5f132084b78db9
ANSI_COLORS = dict(
    bold="\x1b[1m",
    reset="\x1b[0m",
)


class colors:
    """Coloring texts."""

    @staticmethod
    def bold(text):
        return f"{ANSI_COLORS['bold']}{text}{ANSI_COLORS['reset']}"

"""Utilities functions that are needed but re-usable in any projects."""

import logging
import warnings
from typing import Any


def create_success_level() -> None:
    """Create logger.success.

    ref: https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility/35804945#35804945
    """

    def __log_for_level(self: Any, message: Any, *args: Any, **kwargs: Any) -> None:
        """Log for level."""
        if self.isEnabledFor(logging.SUCCESS):
            self._log(logging.SUCCESS, message, args, **kwargs)  # pylint: disable=protected-access

    level_name: str = 'SUCCESS'

    logging.SUCCESS = logging.INFO + 5
    logging.addLevelName(logging.SUCCESS, '\x1b[36;1mSCS\x1b[0m')

    setattr(logging, level_name, logging.SUCCESS)
    setattr(logging.getLoggerClass(), level_name.lower(), __log_for_level)


def disable_internal_loggers() -> None:
    """Disable internal loggers."""

    logging.getLogger('asyncio').setLevel(logging.ERROR)
    warnings.simplefilter('ignore')


def setup_logger(
    verbose_mode: bool = False,
    quiet_mode: bool = False,
) -> logging.Logger:
    """Setup logger."""

    log_level: int = logging.DEBUG if verbose_mode else logging.INFO
    if quiet_mode:
        log_level = logging.ERROR

    log_format: str = '%(asctime)s,%(msecs)04d - %(levelname)s - %(name)s - %(message)s'

    logging.basicConfig(level=log_level, datefmt='%H:%M:%S', format=log_format)

    logging.addLevelName(logging.DEBUG, '\x1b[32;1mDBG\x1b[0m')
    logging.addLevelName(logging.INFO, '\x1b[37;1mINF\x1b[0m')
    logging.addLevelName(logging.WARNING, '\x1b[33;1mWRN\x1b[0m')
    logging.addLevelName(logging.ERROR, '\x1b[31;1mERR\x1b[0m')
    logging.addLevelName(logging.CRITICAL, '\x1b[35;1mCRI\x1b[0m')

    create_success_level()

    disable_internal_loggers()

    return get_logger()


def get_logger(module: str = 'graphinder') -> logging.Logger:
    """Get logger for specified module."""

    return logging.getLogger(module)

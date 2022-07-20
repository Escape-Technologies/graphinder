"""Utilities functions that are needed but re-usable in any projects."""

import logging
import warnings


def disable_internal_loggers() -> None:
    """Disable internal loggers."""

    logging.getLogger('asyncio').setLevel(logging.ERROR)
    warnings.simplefilter('ignore')


def setup_logger(
    verbose_mode: bool = False,
    quiet_mode: bool = False,
    logger: logging.Logger | None = None,
) -> logging.Logger:
    """Setup logger."""

    disable_internal_loggers()

    log_level: int = logging.DEBUG if verbose_mode else logging.INFO
    if quiet_mode:
        log_level = logging.ERROR

    if logger:
        logger = get_logger()
        logger.setLevel(log_level)
        return logger

    log_format: str = '%(asctime)s,%(msecs)04d - %(levelname)s - %(name)s - %(message)s'

    logging.basicConfig(level=log_level, datefmt='%H:%M:%S', format=log_format)

    logging.addLevelName(logging.DEBUG, '\x1b[32;1mDBG\x1b[0m')
    logging.addLevelName(logging.INFO, '\x1b[37;1mINF\x1b[0m')
    logging.addLevelName(logging.WARNING, '\x1b[33;1mWRN\x1b[0m')
    logging.addLevelName(logging.ERROR, '\x1b[31;1mERR\x1b[0m')

    return get_logger()


def get_logger() -> logging.Logger:
    """Get logger for specified module."""

    return logging.getLogger('graphinder')

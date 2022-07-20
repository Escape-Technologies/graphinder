"""Test utils/logger.py."""

import logging
from typing import Any

from graphinder.utils.logger import disable_internal_loggers, get_logger, setup_logger


def test_get_logger() -> None:
    """get_logger test."""

    logger: logging.Logger = get_logger()
    assert logger.name == 'graphinder'

    assert isinstance(logger, logging.Logger)


def test_setup_logger(caplog: Any) -> None:
    """setup_logger test."""

    caplog.set_level(0)

    logger: logging.Logger = setup_logger(False)
    assert logger.name == 'graphinder'

    logger.info('test info')
    logger.debug('test debug')

    assert 'test info' in caplog.text
    assert 'test debug' in caplog.text


def test_disable_internal_loggers(caplog: Any) -> None:
    """disable_internal_loggers test."""

    caplog.set_level(0)

    disable_internal_loggers()
    logger: logging.Logger = logging.getLogger('asyncio')

    logger.info('test info')

    assert 'test info' not in caplog.text

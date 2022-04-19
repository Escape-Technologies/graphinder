"""Test utils/logger.py."""

import logging
from typing import Any

from graphinder.utils.logger import create_success_level, disable_internal_loggers, get_logger, setup_logger


def test_get_logger() -> None:
    """get_logger test."""

    logger: logging.Logger = get_logger('test_get_logger')
    assert logger.name == 'test_get_logger'

    logger = get_logger()
    assert logger.name == 'graphinder'

    assert isinstance(logger, logging.Logger)


def test_setup_logger(caplog: Any) -> None:
    """setup_logger test."""

    caplog.set_level(0)

    logger: logging.Logger = setup_logger(False)
    assert logger.name == 'graphinder'

    logger.info('test info')
    logger.debug('test debug')
    logger.success('test success')

    assert 'test info' in caplog.text
    assert 'test debug' in caplog.text
    assert 'test success' in caplog.text and 'SCS' in caplog.text


def test_disable_internal_loggers(caplog: Any) -> None:
    """disable_internal_loggers test."""

    caplog.set_level(0)

    disable_internal_loggers()
    logger: logging.Logger = get_logger('asyncio')

    logger.info('test info')

    assert 'test info' not in caplog.text


def test_create_success_level() -> None:
    """create_success_level test."""

    create_success_level()

    logger: logging.Logger = get_logger('test_create_success_level')

    assert hasattr(logger, 'success')

    try:
        logger.success('test')
    except AttributeError:
        assert False, 'create_success_level() should add a new level to logging module.'

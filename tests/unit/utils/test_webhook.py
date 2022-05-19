# pylint: disable=redefined-outer-name

"""Test for utils/webhook.py."""

import pytest
from pytest_mock import MockerFixture

from graphinder.entities.io import Results
from graphinder.entities.pool import Url
from graphinder.utils.webhook import format_webhook, send_webhook


@pytest.fixture
def result_one_domain() -> Results:
    """Return a Results object with one domain."""

    return {
        'example.com': {
            Url('http://www.example.com/graphql'),
            Url('http://admin.example.com/graphql'),
        }
    }


@pytest.fixture
def result_multiple_domain() -> Results:
    """Return a Results object with multiples domain."""

    return {
        'example.com': {
            Url('http://www.example.com/graphql'),
            Url('http://admin.example.com/graphql'),
        },
        'example2.com': {
            Url('http://www.example2.com/graphql'),
            Url('http://admin.example2.com/graphql'),
        }
    }


def test_format_webhook_single(result_one_domain: Results) -> None:
    """Test for format_webhook."""

    formatted = format_webhook(result_one_domain)

    assert formatted['username'] == 'Graphinder'
    assert 0 <= formatted['embeds'][0]['color'] <= 16777215
    assert formatted['embeds'][0]['title'] == 'example.com'
    assert formatted['embeds'][0]['description'] == '\n'.join(result_one_domain['example.com'])


def test_format_webhook_multiple(result_multiple_domain: Results) -> None:
    """Test for format_webhook."""

    formatted = format_webhook(result_multiple_domain)

    assert len(formatted['embeds']) == 2


def test_send_webhook(mocker: MockerFixture, result_one_domain: Results) -> None:
    """Test for send_webhook."""

    mocker.patch('requests.post', return_value=mocker.Mock(status_code=204))

    url = 'http://mocked.com/webhook'

    assert send_webhook(url, result_one_domain)

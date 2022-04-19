"""Test utils/assets.py."""

import os
import urllib.request

from graphinder.utils.assets import _compose_subfinder_url, _extract_file, fetch_assets


def test_fetch_assets() -> None:
    """fetch_assets test."""

    path: str = 'subfinder'

    if os.path.isfile(path):
        os.remove(path)

    fetch_assets()
    assert os.path.isfile(path)

    fetch_assets()
    assert os.path.isfile(path)

    if os.path.isfile(path):
        os.remove(path)


def test_extract_file_zip() -> None:
    """_extract_file test for zip."""

    name: str = 'subfinder'

    if os.path.isfile(name):
        os.remove(name)

    url = _compose_subfinder_url('linux', 'amd64')
    urllib.request.urlretrieve(url, f'{name}.zip')
    assert os.path.isfile(f'{name}.zip'), f'{name}.zip not found.'

    _extract_file(f'{name}.zip')

    assert os.path.isfile(name), f'{name} not found.'

    os.remove(f'{name}')
    os.remove(f'{name}.zip')


def test_compose_subfinder_url() -> None:
    """_compose_subfinder_url test."""

    assert _compose_subfinder_url('linux', 'amd64') == 'https://github.com/projectdiscovery/subfinder/releases/download/v2.5.1/subfinder_2.5.1_linux_amd64.zip'
    assert _compose_subfinder_url('darwin', 'amd64') == 'https://github.com/projectdiscovery/subfinder/releases/download/v2.5.1/subfinder_2.5.1_macOS_amd64.zip'
    assert _compose_subfinder_url('win', 'i386') == 'https://github.com/projectdiscovery/subfinder/releases/download/v2.5.1/subfinder_2.5.1_windows_386.zip'
    assert _compose_subfinder_url('darwin', 'arm') == 'https://github.com/projectdiscovery/subfinder/releases/download/v2.5.1/subfinder_2.5.1_macOS_arm64.zip'

    try:
        _compose_subfinder_url('unknown os', 'amd64')
        assert False, 'Expected NotImplementedError.'
    except NotImplementedError:
        pass

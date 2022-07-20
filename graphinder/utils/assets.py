"""Assets utils."""

import os
import platform
import urllib.request
import zipfile

from graphinder.utils.logger import get_logger


def _compose_subfinder_url(
    _os: str = platform.system().lower(),
    _processor: str = platform.processor(),
) -> str:
    """Compose the subfinder url."""

    base_url: str = 'https://github.com/projectdiscovery/subfinder/releases/download/v2.5.1/subfinder_2.5.1_'

    if 'linux' in _os:
        base_url += 'linux'
    elif 'darwin' in _os:
        base_url += 'macOS'
    elif 'win' in _os:
        base_url += 'windows'
    else:
        raise NotImplementedError('OS not supported.')

    if '386' in _processor:
        base_url += '_386'
    elif 'arm' in _processor:
        base_url += '_arm64'
    else:
        base_url += '_amd64'

    return base_url + '.zip'


def _extract_file(file_path: str) -> None:
    """Extract file depending on his extension."""

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall('.')

    os.chmod('subfinder', 0o755)


def fetch_assets() -> None:
    """Fetches the assets."""
    logger = get_logger()

    if os.path.exists('subfinder'):
        logger.debug('subfinder present, skipping.')
        return

    subfinder_url = _compose_subfinder_url()

    logger.info('downloading subfinder...')
    urllib.request.urlretrieve(subfinder_url, 'subfinder.zip')

    logger.info('extracting subfinder...')
    _extract_file('subfinder.zip')

    logger.info('removing subfinder archive...')
    os.remove('subfinder.zip')

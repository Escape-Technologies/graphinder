"""I/O writers."""

import json
import logging
from io import TextIOWrapper
from typing import Any

from graphinder.entities.io import Results


class ResultEncoder(json.JSONEncoder):

    """JSON encoder for `set` type."""

    def default(self, o: Any) -> Any:
        """Encode `set` type."""

        if isinstance(o, set):
            return list(o)
        raise NotImplementedError()


def write_results(output_file: TextIOWrapper | None, results: Results) -> None:
    """Saves the results."""

    if output_file is None:
        logger = logging.getLogger('io')
        logger.debug('no output file specified, skipping writing results..')
        return

    json.dump(results, output_file, indent=4, cls=ResultEncoder, sort_keys=True)

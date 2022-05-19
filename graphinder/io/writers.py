"""I/O writers."""

import json
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


def write_results(output_file: TextIOWrapper, results: Results) -> None:
    """Saves the results."""

    json.dump(
        results,
        output_file,
        indent=4,
        cls=ResultEncoder,
        sort_keys=True,
    )

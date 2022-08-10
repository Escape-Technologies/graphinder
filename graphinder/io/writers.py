"""I/O writers."""

import json
from io import TextIOWrapper
from typing import Any, List

from graphinder.entities.io import Results
from graphinder.utils.filters import transform_url_in_domain


class ResultEncoder(json.JSONEncoder):

    """JSON encoder for `set` type."""

    def default(self, o: Any) -> Any:
        """Encode `set` type."""

        if isinstance(o, set):
            return list(o)
        raise NotImplementedError()


def write_results(
    output_file: TextIOWrapper,
    results: Results,
) -> None:
    """Saves the results."""

    json.dump(
        results,
        output_file,
        indent=4,
        cls=ResultEncoder,
        sort_keys=True,
    )


def write_results_inplace(
    input_file: TextIOWrapper,
    results: Results,
) -> None:
    """Write the result comma separated (as a CSV) into the input file."""

    input_file.seek(0)
    urls: List[str] = list(set(input_file.read().splitlines()))
    final_doc: List[str] = []
    for url in urls:
        clean = transform_url_in_domain(url)
        if clean is not None:
            if clean in results:
                final_doc.append(f'{url},{" ".join(results[clean])}')
        else:
            final_doc.append(url)

    input_file.seek(0)
    input_file.writelines('\n'.join(final_doc))

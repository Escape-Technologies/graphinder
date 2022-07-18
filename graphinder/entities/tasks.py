"""Tasks entities."""

from enum import Enum
from typing import List


class TaskTags(Enum):

    """Task tags."""

    FETCH_SCRIPT = 0
    FETCH_PAGE_SCRIPTS = 1
    FETCH_ENDPOINT = 2


# pylint: disable=too-few-public-methods
class Task:

    """Task representation."""

    def __init__(
        self,
        domain_url: str,
        tag: TaskTags,
        url: str,
    ) -> None:
        """Init task."""

        self.domain_url = domain_url
        self.tag = tag
        self.url = url


TasksList = List[Task]

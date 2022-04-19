"""Test entities/tasks.py."""

from graphinder.entities.tasks import Task, TaskTags


# pylint: disable=no-member,protected-access
def test_tasktags() -> None:
    """TaskTags test."""

    assert len(TaskTags) == 3, 'Excepted 3 different task tags. Please update this test.'

    assert 0 in TaskTags._value2member_map_
    assert 1 in TaskTags._value2member_map_
    assert 2 in TaskTags._value2member_map_


def test_task() -> None:
    """Task test."""

    task: Task = Task('https://example.com', TaskTags.FETCH_SCRIPT, 'https://example.com/script.js')

    assert task.domain_url == 'https://example.com'
    assert task.tag == TaskTags.FETCH_SCRIPT
    assert task.url == 'https://example.com/script.js'

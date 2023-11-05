import logging

from models.task import Task
from models.build import BuildGraphNode


logger = logging.getLogger("data")


def prepare_tasks(tasks: list[Task]) -> dict[str, list[str]]:
    return {task.name: task.dependencies for task in tasks}


def _get_all_tasks_dependencies(
    tasks: list[str],
    tasks_lookup: dict[str, list[str]],
    current_result: set | None = None,
) -> list[str]:
    if current_result is None:
        current_result = set()

    if not tasks:
        return list(current_result)

    new_tasks = []
    for task in tasks:
        new_tasks.extend(tasks_lookup[task])
        current_result.add(task)
    return _get_all_tasks_dependencies(new_tasks, tasks_lookup, current_result)


def create_graph(
    initial_tasks: list[str],
    tasks_lookup: dict[str, list[str]],
) -> dict[str, BuildGraphNode]:
    all_tasks = _get_all_tasks_dependencies(initial_tasks, tasks_lookup)
    new_graph = {
        task: BuildGraphNode(nodes=tasks_lookup[task], degree=len(tasks_lookup[task]))
        for task in all_tasks
    }
    # reverse the graph to get connected nodes
    for key, value in new_graph.items():
        while value.nodes:
            new_item = value.nodes.pop(0)
            new_graph[new_item].nodes.append(key)
    return new_graph

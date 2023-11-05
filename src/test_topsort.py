import copy
import pytest

from models.build import BuildGraphNode
from services.topological_sort import kahn_topsort
from services.prepare_data import create_graph, prepare_tasks
from services.yaml_ops import read_builds, read_tasks


def get_params_from_initial_data() -> list[dict[str, BuildGraphNode]]:
    params = []
    tasks = read_tasks()
    builds = read_builds()
    tasks_lookup = prepare_tasks(tasks.tasks)
    for build in builds.builds:
        graph = create_graph(build.tasks, tasks_lookup)
        params.append(graph)
    return params


def verify_topsort(sorted_nodes: list[str], graph: dict[str, BuildGraphNode]):
    for node in sorted_nodes:
        # delete current node
        node_value = graph.pop(node)
        assert node_value.degree == 0
        # update degree for connected nodes
        for connected_node in node_value.nodes:
            graph[connected_node].degree -= 1


@pytest.mark.parametrize(
    "graph",
    [
        {
            "a": BuildGraphNode(degree=0, nodes=["b"]),
            "b": BuildGraphNode(degree=1, nodes=["c"]),
            "c": BuildGraphNode(degree=1, nodes=[]),
        },
        {
            "a": BuildGraphNode(degree=0, nodes=["b"]),
            "b": BuildGraphNode(degree=1, nodes=["c"]),
            "c": BuildGraphNode(degree=2, nodes=[]),
            "d": BuildGraphNode(degree=0, nodes=["c"]),
        },
        {
            "a": BuildGraphNode(degree=0, nodes=["b"]),
            "b": BuildGraphNode(degree=1, nodes=["c"]),
            "c": BuildGraphNode(degree=4, nodes=[]),
            "d": BuildGraphNode(degree=0, nodes=["c"]),
            "e": BuildGraphNode(degree=0, nodes=["c"]),
            "f": BuildGraphNode(degree=0, nodes=["c"]),
        },
        {
            "a": BuildGraphNode(degree=0, nodes=["b"]),
            "b": BuildGraphNode(degree=1, nodes=["c"]),
            "c": BuildGraphNode(degree=4, nodes=[]),
            "d": BuildGraphNode(degree=1, nodes=["c"]),
            "e": BuildGraphNode(degree=1, nodes=["c"]),
            "f": BuildGraphNode(degree=1, nodes=["c"]),
            "g": BuildGraphNode(degree=0, nodes=["d"]),
            "h": BuildGraphNode(degree=0, nodes=["e"]),
            "i": BuildGraphNode(degree=0, nodes=["f"]),
        },
        {
            "a": BuildGraphNode(degree=0, nodes=["b", "g"]),
            "b": BuildGraphNode(degree=1, nodes=["c"]),
            "c": BuildGraphNode(degree=4, nodes=[]),
            "d": BuildGraphNode(degree=1, nodes=["c"]),
            "e": BuildGraphNode(degree=1, nodes=["c"]),
            "f": BuildGraphNode(degree=1, nodes=["c"]),
            "g": BuildGraphNode(degree=1, nodes=["d", "h"]),
            "h": BuildGraphNode(degree=1, nodes=["e", "i"]),
            "i": BuildGraphNode(degree=1, nodes=["f"]),
        },
        {
            "a": BuildGraphNode(degree=0, nodes=["b", "g", "d"]),
            "b": BuildGraphNode(degree=1, nodes=["c"]),
            "c": BuildGraphNode(degree=4, nodes=[]),
            "d": BuildGraphNode(degree=2, nodes=["c"]),
            "e": BuildGraphNode(degree=3, nodes=["c"]),
            "f": BuildGraphNode(degree=1, nodes=["c"]),
            "g": BuildGraphNode(degree=1, nodes=["d", "h", "e"]),
            "h": BuildGraphNode(degree=1, nodes=["e", "i"]),
            "i": BuildGraphNode(degree=1, nodes=["f", "e"]),
        },
        *get_params_from_initial_data(),
    ],
)
def test_topsort_algorithm(graph: dict[str, BuildGraphNode]):
    sorted_graph = kahn_topsort(copy.deepcopy(graph))
    verify_topsort(sorted_graph, graph)

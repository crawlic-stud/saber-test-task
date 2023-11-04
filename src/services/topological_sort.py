from collections import deque

from models.build import BuildGraphNode


def kahn_topsort(graph: dict[str, BuildGraphNode]) -> list[str]:
    graph_length = len(graph)
    q = deque(maxlen=graph_length)

    for key, value in graph.items():
        if value.degree == 0:
            q.append(key)

    order = []
    while q:
        node: str = q.popleft()
        order.append(node)
        for next_node in graph[node].nodes:
            graph[next_node].degree -= 1
            if graph[next_node].degree == 0:
                q.append(next_node)
    return order

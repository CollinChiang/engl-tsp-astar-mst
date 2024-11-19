import heapq

from utils import calculate, timeit


def mst(N, A, nodes: list[int]):
    """
    Adapted from: https://www.geeksforgeeks.org/prims-minimum-spanning-tree-mst-greedy-algo-5/
    """
    # calculates the minimum spanning tree (prim's algorithm)
    length = len(nodes)
    queue = []

    # trivial case, there are no nodes left
    if length == 0:
        return 0

    node = nodes.pop(0)
    search = A[node]
    for other in nodes:
        heapq.heappush(queue, (search[other], other))

    # visit all nodes and add to spanning tree
    cost = 0
    visited = [node]
    while len(visited) < length:
        weight, node = heapq.heappop(queue)

        # removes already visited nodes
        if node in visited:
            continue

        # visit the node
        nodes.remove(node)
        visited.append(node)

        # search for nearest
        search = A[node]
        for other in nodes:
            heapq.heappush(queue, (search[other], other))

        # updates cost
        cost += weight

    return cost


@timeit
def _A_MST(N, A):
    memorize = {}
    nodes: set[int] = set(range(N))

    queue = []
    heapq.heappush(queue, (mst(N, A, list(nodes)), [0]))

    expanded = 0

    # creates an empty path
    result = []
    while len(queue) > 0:
        cost, order = heapq.heappop(queue)

        # keeps track of nodes expanded
        expanded += 1

        # determines if we have returned to start
        if len(order) == N:
            cost = calculate(N, A, order)
            heapq.heappush(queue, (cost, order + [0]))
            continue

        # termination step, we've popped the result
        if len(order) == N + 1:
            result = order[:N]
            break

        # determines which nodes to visit
        visiting = nodes.difference(set(order))
        for node in visiting:
            lst = frozenset(visiting.difference({node}))

            space = order.copy()
            space.append(node)

            # speedup: memorize remaining spanning trees
            if lst not in memorize.keys():
                memorize[lst] = mst(N, A, list(lst) + [0])

            cost = memorize[lst] + calculate(N, A, order, complete=False)
            heapq.heappush(queue, (cost, space))

    return expanded, calculate(N, A, result)


def A_MST(N, A):
    cpu, real, (nodes, cost) = _A_MST(N, A)
    return cpu, real, nodes, cost

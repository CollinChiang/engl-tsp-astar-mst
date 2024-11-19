import time


def timeit(x):
    def _timeit(*args, **kwargs):
        cpu0 = time.process_time_ns()
        real0 = time.perf_counter_ns()

        result = x(*args, **kwargs)

        cpu1 = time.process_time_ns()
        real1 = time.perf_counter_ns()

        cpu = cpu1 - cpu0
        real = real1 - real0

        return cpu, real, result

    return _timeit


def calculate(N, A, x, complete=True):
    if complete:
        assert len(x) == N

    x0 = x[0]
    cost = 0
    for index in range(1, len(x)):
        cost += A[x[index - 1]][x[index]]

    if complete:
        cost += A[x[N - 1]][x0]

    return float(cost)

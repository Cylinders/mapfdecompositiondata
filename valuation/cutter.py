from typing import TypeVar

T = TypeVar("T")


def no_cut(agents: list[T]) -> list[list[list[T]]]:
    return [[agents]]


def half_cut(agents: list[T]) -> list[list[list[T]]]:
    mid = len(agents) // 2

    return [[
        agents[:mid],
        agents[mid:],
    ]]


def n_cut(n: int, agents: list[T]) -> list[list[list[T]]]:
    assert n > 0

    k, r = divmod(len(agents), n)

    cut: list[list[T]] = []
    start = 0

    for i in range(n):
        size = k + (1 if i < r else 0)
        cut.append(agents[start:start + size])
        start += size

    return [cut]


def up_to_n_cuts(n: int, agents: list[T]) -> list[list[list[T]]]:
    return [n_cut(n, agents)[0] for n in range(1, n + 1)]


def epsilon_cut(epsilon: int, agents: list[T]) -> list[list[list[T]]]:
    return

"""
Benchmark recursive generators implemented in python
by traversing a binary tree.

Author: Kumar Aditya
"""

from __future__ import annotations

from collections.abc import Iterator

import pyperf


class Tree:
    def __init__(self, left: Tree | None, value: int, right: Tree | None) -> None:
        self.left = left
        self.value = value
        self.right = right

    def __iter__(self) -> Iterator[int]:
        if self.left:
            yield from self.left
        yield self.value
        if self.right:
            yield from self.right


def tree(input: range) -> Tree | None:
    n = len(input)
    if n == 0:
        return None
    i = n // 2
    return Tree(tree(input[:i]), input[i], tree(input[i + 1:]))

def bench_generators(loops: int) -> float:
    assert list(tree(range(10))) == list(range(10))
    range_it = range(loops)
    iterable = tree(range(100000))
    t0 = pyperf.perf_counter()
    for _ in range_it:
        for _ in iterable:
            pass
    return pyperf.perf_counter() - t0

if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata['description'] = "Benchmark generators"

    cds_mode = None
    try:
        import cds
        cds_mode = cds._cds.flags.mode
    except ImportError:
        pass

    if cds_mode == 1:
        bench_generators(1)
    else:
        runner.bench_time_func('generators', bench_generators)

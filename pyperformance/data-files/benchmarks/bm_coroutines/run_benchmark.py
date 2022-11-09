"""
Benchmark for recursive coroutines.

Author: Kumar Aditya
"""

import pyperf


async def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return await fibonacci(n - 1) + await fibonacci(n - 2)


def bench_coroutines(loops: int) -> float:
    range_it = range(loops)
    t0 = pyperf.perf_counter()
    for _ in range_it:
        coro = fibonacci(25)
        try:
            while True:
                coro.send(None)
        except StopIteration:
            pass
    return pyperf.perf_counter() - t0


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata['description'] = "Benchmark coroutines"

    cds_mode = None
    try:
        import cds
        cds_mode = cds._cds.flags.mode
    except ImportError:
        pass

    if cds_mode == 1:
        bench_coroutines(1)
    else:
        runner.bench_time_func('coroutines', bench_coroutines)

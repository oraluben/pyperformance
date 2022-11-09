"""
Benchmark for concurrent model communication.
"""
import pyperf

from multiprocessing.pool import Pool, ThreadPool


def f(x: int) -> int:
    return x


def bench_mp_pool(p: int, n: int, chunk: int) -> None:
    with Pool(p) as pool:
        for _ in pool.imap(f, range(n), chunk):
            pass


def bench_thread_pool(c: int, n: int, chunk: int) -> None:
    with ThreadPool(c) as pool:
        for _ in pool.imap(f, range(n), chunk):
            pass


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata["description"] = "concurrent model communication benchmark"
    count = 1000
    chunk = 10
    num_core = 2

    cds_mode = None
    try:
        import cds
        cds_mode = cds._cds.flags.mode
    except ImportError:
        pass

    if cds_mode == 1:
        bench_mp_pool(num_core, count, chunk)
        bench_thread_pool(num_core, count, chunk)
    else:
        runner.bench_func("bench_mp_pool", bench_mp_pool, num_core, count, chunk)
        runner.bench_func("bench_thread_pool", bench_thread_pool, num_core, count, chunk)

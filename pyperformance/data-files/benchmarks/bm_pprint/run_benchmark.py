"""Test the performance of pprint.PrettyPrinter.

This benchmark was available as `python -m pprint` until Python 3.12.

Authors: Fred Drake (original), Oleg Iarygin (pyperformance port).
"""

import pyperf
from pprint import PrettyPrinter


printable = [('string', (1, 2), [3, 4], {5: 6, 7: 8})] * 100_000
p = PrettyPrinter()


if __name__ == '__main__':
    runner = pyperf.Runner()
    runner.metadata['description'] = 'pprint benchmark'

    cds_mode = None
    try:
        import cds
        cds_mode = cds._cds.flags.mode
    except ImportError:
        pass

    if cds_mode == 1:
        if hasattr(p, '_safe_repr'):
            p._safe_repr(printable, {}, None, 0)
        p.pformat(printable)
    else:
        if hasattr(p, '_safe_repr'):
            runner.bench_func('pprint_safe_repr', p._safe_repr,
                              printable, {}, None, 0)
        runner.bench_func('pprint_pformat', p.pformat, printable)

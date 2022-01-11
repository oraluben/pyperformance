import glob
import os.path
import sys

import pyperf


if __name__ == "__main__":
    runner = pyperf.Runner()

    runner.metadata['description'] = "Performance of the Python 2to3 program"
    args = runner.parse_args()

    datadir = os.path.join(os.path.dirname(__file__), 'data', '2to3')
    pyfiles = glob.glob(os.path.join(datadir, '*.py.txt'))

    command = [sys.executable, "-m", "lib2to3", "-f", "all"] + pyfiles

    cds_mode = None
    try:
        import cds
        cds_mode = cds._cds.flags.mode
    except ImportError:
        pass

    if cds_mode == 1:
        from subprocess import run, DEVNULL

        run(command, env={'PYCDSMODE': 'TRACE', 'PYCDSLIST': 'test.lst'}, stdout=DEVNULL, stderr=DEVNULL)
    else:
        runner.bench_command('2to3', command)

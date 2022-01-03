from load_functions import *
import math
import os
import time

def experiments(
    folder = "dataset",
    max_num_files = None,
    tries = 3,
    skip_after = 10.0,
    skip = [],
    ):

    times = {
        'python': [],
        'julia_c': [],
        'julia_basic': [],
        'julia_prealloc': [],
        'julia_opt': [],
        'cpp': [],
        'load_external': [],
    }

    elements = []
    rows = []

    files = sorted(os.scandir(folder), key=lambda x: x.name)
    N = len(list(files))
    if max_num_files is None or max_num_files <= 0:
        max_num_files = N
    else:
        N = min(N, max_num_files)
    offenders = []

    for i, filename in enumerate(files):
        if i >= max_num_files:
            break
        filename = filename.path
        # Complete Python
        if 'python' in skip:
            times['python'].append(math.nan)
        else:
            start = time.time()
            for _ in range(0, tries):
                df = load_pandas(filename)
            times['python'].append((time.time() - start) / tries)

        # Separate read
        for (key, read_fun) in [
                ('julia_c',     read_arrays_julia_c),
                ('julia_basic', read_arrays_julia_basic),
                ('julia_prealloc', read_arrays_julia_prealloc),
                ('julia_opt',   read_arrays_julia_opt),
                ('cpp',         read_arrays_cpp),
            ]:
            if key in skip:
                times[key].append(math.nan)
            else:
                start = time.time()
                for _ in range(0, tries):
                    arrays = read_fun(filename)
                times[key].append((time.time() - start) / tries)

        # External load
        start = time.time()
        for _ in range(0, tries):
            df = load_external(arrays)
        elements.append(df.shape[0])
        rows.append(sum(1 for _ in open(filename)))
        times['load_external'].append((time.time() - start) / tries)

        # Slow part
        if tries > 1 and times['load_external'][-1] > 0.01:
            tries = 1
        for k in times.keys() - ['load_external']:
            if times[k][-1] > skip_after:
                if k in offenders:
                    skip.append(k)
                else:
                    offenders.append(k)

        # Progress
        perc = round(100 * (i + 1) / N, 1)
        print(f'progress = {perc}%, file {filename}')
        print('  ' + ' '.join([f'{k}:{v[-1]}' for k, v in times.items()]))

    df = pd.DataFrame({
        'elements': elements,
        'rows': rows,
        **times,
    })
    df.to_csv('out/experiments.csv', index=False)
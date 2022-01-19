from load_functions import *
import math
import os
import time

def experiments(
    folder = "dataset",
    max_num_files = 0,
    tries = 3,
    skip_after = 0.0,
    skip = [],
    ):

    times = {
        'python': [],
        'pandas_read_csv': [],
        'pandas_tuples_to_df': [],
        'julia_basic': [],
        'julia_prealloc': [],
        'cpp': [],
        'load_external': [],
    }

    elements = []
    rows = []

    files = sorted(os.scandir(folder), key=lambda x: x.name)
    files = list(filter(lambda x: os.path.splitext(x)[1] != '.csv', files))
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
            times['pandas_read_csv'].append(math.nan)
            times['pandas_tuples_to_df'].append(math.nan)
        else:
            try:
                print(f'Running python')
                start = time.time()
                for _ in range(0, tries):
                    df_tuples = pandas_read_csv(filename)
                times['pandas_read_csv'].append((time.time() - start) / tries)

                start = time.time()
                for _ in range(0, tries):
                    df = pandas_tuple_to_dataframe(df_tuples)
                times['pandas_tuples_to_df'].append((time.time() - start) / tries)
            except:
                times['pandas_read_csv'].append(math.nan)
                times['pandas_tuples_to_df'].append(math.nan)

        times['python'].append(times['pandas_read_csv'][-1] + times['pandas_tuples_to_df'][-1])

        # Separate read
        for (key, read_fun) in [
                ('julia_basic', read_arrays_julia_basic),
                ('julia_prealloc', read_arrays_julia_prealloc),
                ('cpp',         read_arrays_cpp),
            ]:
            print(f'Running {key}')
            if key in skip:
                times[key].append(math.nan)
            else:
                try:
                    start = time.time()
                    for _ in range(0, tries):
                        arrays = read_fun(filename)
                    times[key].append((time.time() - start) / tries)
                    if len(arrays[0]) == 0: # Actually failed
                        times[key][-1] = math.nan
                except:
                    times[key].append(math.nan)

        # External load
        start = time.time()
        for _ in range(0, tries):
            df = load_external(arrays)
        times['load_external'].append((time.time() - start) / tries)

        elements.append(df.shape[0])
        rows.append(sum(1 for _ in open(filename)))

        for k in times.keys() - ['load_external']:
            if skip_after > 0 and times[k][-1] > skip_after:
                if k in offenders:
                    skip.append(k)
                else:
                    offenders.append(k)

        # Progress
        perc = round(100 * (i + 1) / N, 1)
        print(f'progress = {perc}%, file {filename}')
        print('  ' + ' '.join([f'{k}:{round(v[-1], 4)}' for k, v in times.items()]))

        df = pd.DataFrame({
            'elements': elements,
            'rows': rows,
            **times,
        })
        df.to_csv('out/experiments.csv', index=False)
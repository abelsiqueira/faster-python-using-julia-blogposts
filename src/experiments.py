from load_functions import *
import os
import time

def experiments(
    folder = "gen-data",
    max_num_files = None,
    tries = 3,
    ):

    times = {
        'pure_python': [],
        'julia_c': [],
        'julia_basic': [],
        'julia_opt': [],
        'cpp': [],
        'load_external': [],
    }

    elements = []

    files = sorted(os.scandir(folder), key=lambda x: x.name)
    N = len(list(files))
    if max_num_files is None:
        max_num_files = N
    else:
        N = min(N, max_num_files)

    for i, filename in enumerate(files):
        if i >= max_num_files:
            break
        filename = filename.path
        # Complete Python
        start = time.time()
        for _ in range(0, tries):
            df = load_pandas(filename)
        times['pure_python'].append((time.time() - start) / tries)

        elements.append(df.shape[0])

        # Separate read
        for (key, read_fun) in [
                ('julia_c',     read_arrays_julia_c),
                ('julia_basic', read_arrays_julia_basic),
                ('julia_opt',   read_arrays_julia_opt),
                ('cpp',         read_arrays_cpp),
            ]:
            start = time.time()
            for _ in range(0, tries):
                arrays = read_fun(filename)
            times[key].append((time.time() - start) / tries)

        # External load
        start = time.time()
        for _ in range(0, tries):
            df = load_external(arrays)
        times['load_external'].append((time.time() - start) / tries)

        # Slow part
        if tries > 1 and times['load_external'][-1] > 1.0:
            tries = 1

        # Progress
        perc = round(100 * (i + 1) / N, 1)
        print(f'progress = {perc}%, file {filename}')

    df = pd.DataFrame({
        'elements': elements,
        **times,
    })
    df.to_csv('out/experiments.csv', index=False)
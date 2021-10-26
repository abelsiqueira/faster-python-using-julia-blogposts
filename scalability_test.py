#%%
# Preparing the Julia part:
# - You need Python with a shared library! (Arch Linux /usr/bin/python)
# - Tested on Julia 1.6.3
# - Open Julia, enter the following commands:
#   - julia> using Pkg
#   - ENV["PYTHON"] = "/path/to/python"
#   - Pkg.add("PyCall")
# - Install pyjulia with `python -m pip install julia`
# - Run `python`, `import julia`, then `julia.install("julia=julia-1.6.3")` or whatever it's called.
#   - The argument of `install` can be ignored it `julia` is your binary.

import numpy as np
import pandas as pd
import time

### PYTHON ###
def load_pandas(filename):
    df_tuples = pd.read_csv(filename,
                        sep='#', index_col=0, names=['key', 'values'],
                        converters={'values': lambda w: tuple(w.split(','))})
    df = df_tuples['values'].apply(pd.Series, 1).stack().astype('uint64').to_frame()
    df.index.rename(["key", "list_index"], inplace=True)
    df.rename({0: 'value'}, axis='columns', inplace=True)
    return df

### JULIA ###
import julia
from julia.api import Julia
jl = Julia(runtime="julia-1.6.3")
from julia import Main
jl.eval('include("jl_reader.jl")')
jl.eval('include("jl_reader_pure.jl")')
def load_jl(jl_index):
    df = pd.DataFrame.from_records({"key": jl_index[0],
                                   "list_index": jl_index[1],
                                   "value": jl_index[2]}, index=["key", "list_index"])
    return df

### C++ ###
import ticcl_output_reader
def load_cpp(filename):
    cpp_index = ticcl_output_reader.load_confuslist_index(filename)
    df = pd.DataFrame.from_records({"key": cpp_index[0],
                                   "list_index": cpp_index[1],
                                   "value": cpp_index[2]}, index=["key", "list_index"])
    return df

#%% Warmup
filename = "gen-data/confus-001-0.txt"
Main.filename = filename
df_python = load_pandas(filename)
df_julia_and_c = load_jl(jl.eval(f'load_confusjl(filename)'))
df_julia = load_jl(jl.eval(f'load_confus_purejl(filename)'))
df_cpp = load_cpp(filename)

#%%
python_time = []
cpp_time = []
julia_and_c_time = []
julia_time = []
rows = []
elements = []

N = 50
for i in range(1, N + 1):
    for j in range(0, 10):
        filename = 'gen-data/confus-{:03d}-{}.txt'.format(i, j)
        Main.filename = filename
        start = time.time()
        df_python = load_pandas(filename)
        python_time.append(time.time() - start)
        start = time.time()
        df_cpp = load_cpp(filename)
        cpp_time.append(time.time() - start)
        start = time.time()
        df_julia_and_c = load_jl(jl.eval(f'load_confusjl(filename)'))
        julia_and_c_time.append(time.time() - start)
        start = time.time()
        df_julia = load_jl(jl.eval(f'load_confus_purejl(filename)'))
        julia_time.append(time.time() - start)
        rows.append(5 * i)
        elements.append(df_julia.shape[0])
        perc = round(100 * (i * 10 + j) / ((N + 1) * 10 - 1), 1)
        print(f'perc = {perc}%')

df = pd.DataFrame({
    'rows': rows,
    'elements': elements,
    'python_time': python_time,
    'cpp_time': cpp_time,
    'julia_and_c_time': julia_and_c_time,
    'julia_time': julia_time,
})
df.to_csv('scalability_test.csv')
# %%

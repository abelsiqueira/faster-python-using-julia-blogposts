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

# filename = "input_simple.txt"
filename = "pandas_loading_benchmarks_data.txt"
# filename = "confus.txt"

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
Main.filename = filename
jl.eval('include("jl_reader.jl")')
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

#%%
df_python = load_pandas(filename)
df_julia = load_jl(jl.eval(f'load_confusjl(filename)'))
df_cpp = load_cpp(filename)

df_python.shape, df_julia.shape, df_cpp.shape
#%%

df_python.eq(df_julia).all().all(), df_python.eq(df_cpp).all().all()
#%%
%timeit load_pandas(filename)
#%%
%timeit load_cpp(filename)
# %%
%timeit load_jl(jl.eval('load_confusjl(filename)'))
# %%

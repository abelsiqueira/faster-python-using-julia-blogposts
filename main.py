#%%
# Preparing the Julia part:
# - You need Python 3.8 with a shared library! (Arch Linux AUR python38)
# - You need Julia 1.5.3
# - Open Julia, enter the following commands:
#   - julia> using Pkg
#   - ENV["PYTHON"] = "/path/to/python3.8"
#   - Pkg.add("PyCall")
# - Install pyjulia with `python3.8 -m pip install julia`

import numpy as np
import pandas as pd

# filename = "pandas_loading_benchmarks_data.txt"
filename = "confus.txt"

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
jl = Julia(runtime="julia-1.5.3")
# jl = Julia(runtime="julia-1.5.3", compiled_modules=False)
from julia import Main
Main.filename = filename
jl.eval('include("jl_reader.jl")')
def load_jl(jl_index):
    df = pd.DataFrame.from_records({"key": jl_index[0],
                                   "list_index": jl_index[1],
                                   "value": jl_index[2]}, index=["key", "list_index"])
    return df

### C++ ###
# import ticcl_output_reader
# def load_cpp(filename):
#     cpp_index = ticcl_output_reader.load_confuslist_index(filename)
#     df = pd.DataFrame.from_records({"key": cpp_index[0],
#                                    "list_index": cpp_index[1],
#                                    "value": cpp_index[2]}, index=["key", "list_index"])
#     return df

#%%
df_python = load_pandas(filename)
df_julia = load_jl(jl.eval(f'load_confusjl(filename)'))

df_python.compare(df_julia)
#%%
%timeit load_pandas(filename)
# %%
%timeit load_jl(jl.eval('load_confusjl(filename)'))
# %%
%timeit jl.eval('load_confusjl(filename)')
# %%

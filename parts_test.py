import numpy as np
import pandas as pd
import time

### C++ ###
import ticcl_output_reader

### JULIA ###
import julia
from julia.api import Julia
jl = Julia(runtime="julia-1.6.3")
from julia import Main
jl.eval('include("jl_reader_c.jl")')
jl.eval('include("jl_reader_dict.jl")')
jl.eval('include("jl_reader_manual.jl")')
def load(jl_index):
    df = pd.DataFrame.from_records({"key": jl_index[0],
                                   "list_index": jl_index[1],
                                   "value": jl_index[2]}, index=["key", "list_index"])
    return df

#%% Warmup
filename = "gen-data/confus-001-0.txt"
Main.filename = filename
df_julia_and_c = load(jl.eval(f'load_confusjl(filename)'))
df_julia = load(jl.eval(f'load_confus_purejl(filename)'))
df_cpp = load(ticcl_output_reader.load_confuslist_index(filename))

#%%
load_time = []
julia_and_c_time = []
pure_julia_time = []
cpp_time = []
rows = []
elements = []

N = 100
for i in range(1, N + 1):
    for j in range(0, 10):
        filename = 'gen-data/confus-{:03d}-{}.txt'.format(i, j)
        Main.filename = filename

        start = time.time()
        ticcl_output_reader.load_confuslist_index(filename)
        cpp_time.append(time.time() - start)

        start = time.time()
        jl.eval(f'load_confusjl(filename)')
        julia_and_c_time.append(time.time() - start)

        start = time.time()
        jl.eval(f'load_confus_purejl(filename)')
        pure_julia_time.append(time.time() - start)

        jl_index = jl.eval(f'load_confus_purejl(filename)')

        start = time.time()
        df = load(jl_index)
        load_time.append(time.time() - start)

        rows.append(5 * i)
        elements.append(df.shape[0])
        perc = round(100 * (i * 10 + j) / ((N + 1) * 10 - 1), 1)
        print(f'perc = {perc}%')

df = pd.DataFrame({
    'rows': rows,
    'elements': elements,
    'julia_and_c_time': julia_and_c_time,
    'pure_julia_time': pure_julia_time,
    'cpp_time': cpp_time,
    'load_time': load_time,
})
df.to_csv('parts_test.csv')
# %%

import julia
import pandas as pd
import ticcl_output_reader

from julia.api import Julia
jl = Julia(runtime="julia-1.6.4")
jl.eval('using Pkg')
jl.eval('Pkg.activate(".")')
from julia import Main
jl.eval('include("src/julia/jl_reader_c.jl")')
jl.eval('include("src/julia/jl_reader_basic.jl")')
jl.eval('include("src/julia/jl_reader_prealloc.jl")')
jl.eval('include("src/julia/jl_reader_opt.jl")')

def pandas_read_csv(filename):
    df_tuples = pd.read_csv(filename,
                        sep='#', index_col=0, names=['key', 'elements'],
                        converters={'elements': lambda w: tuple(w.split(','))})
    return df_tuples

def pandas_tuple_to_dataframe(df_tuples):
    df = df_tuples['elements'].apply(pd.Series, 1).stack().astype('uint64').to_frame()
    df.index.rename(["key", "index"], inplace=True)
    df.rename({0: 'element'}, axis='columns', inplace=True)
    return df

def load_pandas(filename):
    return pandas_tuple_to_dataframe(pandas_read_csv(filename))

def load_external(arrays):
    df = pd.DataFrame.from_records({
            "key": arrays[0],
            "index": arrays[1],
            "element": arrays[2]
        }, index=["key", "index"])
    return df

def read_arrays_julia_c(filename):
    return jl.eval(f'read_arrays_jl_c("{filename}")')

def read_arrays_julia_basic(filename):
    return jl.eval(f'read_arrays_jl_basic("{filename}")')

def read_arrays_julia_prealloc(filename):
    return jl.eval(f'read_arrays_jl_prealloc("{filename}")')

def read_arrays_julia_opt(filename):
    return jl.eval(f'read_arrays_jl_opt("{filename}")')

def read_arrays_cpp(filename):
    return ticcl_output_reader.load_confuslist_index(filename)
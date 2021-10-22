#%%
import ticcl_output_reader
import numpy as np
import pandas as pd

filename = "confus.txt"

def load_cpp(filename):
    cpp_index = ticcl_output_reader.load_confuslist_index(filename)
    df = pd.DataFrame.from_records({"key": cpp_index[0],
                                   "list_index": cpp_index[1],
                                   "value": cpp_index[2]}, index=["key", "list_index"])
    return df

# %%
load_cpp(filename)
# %%
%timeit load_cpp(filename)

import argparse
from pathlib import Path
import math

from experiments import experiments
from load_functions import *
from analysis import *

parser = argparse.ArgumentParser()
parser.add_argument('--folder', type=str, help='Folder containing the problem set', default='gen-data')
parser.add_argument('--max-num-files', type=int, help='Limit the number of files to be read from the folder.', default=math.inf)

args = parser.parse_args()

Path("out").mkdir(exist_ok=True)

filename = "gen-data/confus-001-0.txt"
df_python = load_pandas(filename)
df_julia_c = load_external(read_arrays_julia_c(filename))
df_julia_dict = load_external(read_arrays_julia_basic(filename))
df_julia_manual = load_external(read_arrays_julia_opt(filename))
df_cpp = load_external(read_arrays_cpp(filename))

assert df_python.eq(df_julia_c).all().all()
assert df_python.eq(df_julia_dict).all().all()
assert df_python.eq(df_julia_manual).all().all()
assert df_python.eq(df_cpp).all().all()

experiments(
    folder = args.folder,
    max_num_files = args.max_num_files,
)

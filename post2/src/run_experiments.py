
import argparse
from pathlib import Path
import math
import os

from experiments import experiments
from load_functions import *
from analysis import *
# analysis define spc_args

parser = argparse.ArgumentParser()
parser.add_argument('--folder', type=str, help='Folder containing the problem set', default='dataset')
parser.add_argument('--max-num-files', type=int, help='Limit the number of files to be read from the folder. Set to 0 to read all.', default=0)
parser.add_argument('--skip-after', type=float, help='Time threshold to skip the tests of a language. The second time a language run takes more than this threshold, no more tests for this language are done. Set to 0 to disable. (Default = 0)', default=0.0)
parser.add_argument('--skip', type=str, nargs='+', help='Languages to skip. Possible values are {}'.format(', '.join(spc_args)), default=[])

args = parser.parse_args()

Path("out").mkdir(exist_ok=True)

files = sorted(os.scandir(args.folder), key=lambda x: x.name)
filename = files[0].path
# TODO: Check the skip file to avoid these comparisons
df_python = load_pandas(filename)
df_julia_basic = load_external(read_arrays_julia_basic(filename))
df_julia_prealloc = load_external(read_arrays_julia_prealloc(filename))
df_cpp = load_external(read_arrays_cpp(filename))

assert df_python.eq(df_julia_basic).all().all()
assert df_python.eq(df_julia_prealloc).all().all()
assert df_python.eq(df_cpp).all().all()

experiments(
    folder = args.folder,
    max_num_files = args.max_num_files,
    skip_after = args.skip_after,
    skip = args.skip,
)

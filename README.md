# Calling Julia from Python - an experiment on data loading

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5708268.svg)](https://doi.org/10.5281/zenodo.5708268)

See the [slides](slides).

## TLDR

After reading [Patrick's blog post][patrick], we decided to try to replace C++ with Julia to check:
- How easy/hard it is
- How much improvement can be gained with a basic version
- How much improvement can be gained with an optimized version

A basic version is already an improvement over the pure Python version, and an optimized version was faster than the C++ version. Here's a plot comparison all the versions:

<img src="https://github.com/abelsiqueira/call-julia-from-python-experiments/assets/comparison.png" width="49%">
<img src="https://github.com/abelsiqueira/call-julia-from-python-experiments/assets/comparison-relative.png" width="49%">

The versions are:

- Pure Python: Python using Pandas.
- C++: Python and C++.
- Basic Julia: Basic Julia version with mostly disregard for efficiency.
- Prealloc Julia: Julia version trying to improve memory usage.
- Julia + C parsing: Julia version where the elements are read with `fscanf` from C.
- Optimized Julia: Julia version reading the file as bytes and manually walking through the bytes.

## Reproduction

- Download dataset and store in a folder called `dataset`: [![Zenodo badge][dataset-badge]][dataset]
- Get the image with
  ```
  docker pull abelsiqueira/jl-from-py:0.3.0
  ```
- Run it with
  ```
  docker run --rm --volume "$PWD/dataset:/app/dataset" --volume "$PWD/out:/app/out" jl-from-py:0.3.0 --max-num-files 0
  ```
- You will find the output in the `out/` folder.

The docker runs the script `src/main.py` that runs `run_experiments.py` and `run_analysis.py`.

### Arguments

- `--folder FOLDER`: Set the dataset folder. (Default: `dataset`).
- `--max-num-files N`: Maximum number of files to read from can be used to limit the experiment. The files are traversed in sorted name order. Use 0 or a negative number to run all. (Default: `0`).
- `--skip-after X`: Time threshold in seconds to skip the tests of a specific version. If the threshold is reached twice, that version is skipped in the additional tests. (Default: `10`).
- `--skip VALUE1 [VALUE2 ...]`: List of versions to skip. Valid values: `python`, `cpp`, `julia_basic`, `julia_c`, `julia_prealloc`, `julia_opt`.

[patrick]: https://blog.esciencecenter.nl/irregular-data-in-pandas-using-c-88ce311cb9ef
[dataset]: https://zenodo.org/record/5816746
[dataset-badge]: https://zenodo.org/badge/DOI/10.5281/zenodo.5816746.svg

# Calling Julia from Python - an experiment on data loading

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5708268.svg)](https://doi.org/10.5281/zenodo.5708268)

This material is part of a benchmark study about using Julia from Python.
The idea was initially presented internally (See the [slides](slides)).
We are turning it into a blog post that will be released soon.

## Summary

- We read [Patrick's blog post][patrick] about improving the reading of irregular files.
- Patrick has a Python (Pandas) code that is slow.
- Using some packages, he moves the reading and parsing to C++.
- We decided to try to replace C++ with Julia to check:
  - How easy/hard it is
  - How much improvement can be gained with a basic Julia code;
  - How much further improvement can be gained with an optimized Julia code.

The cases we examined are below, with a plot with the comparison following it:

- Python with Pandas, as seen in Patrick's post. label: "Pure Python".
- Python with reading and parsing in C++, as seen in Patrick's post. label: "C++".
- Python with reading and parsing in Julia, in 4 different versions:
  - Basic Julia version with mostly disregard for efficiency, label="Basic Julia".
  - Julia version trying to improve memory usage. label: "Prealloc Julia".
  - Julia version where the elements are read with `fscanf` from C. label: "Julia + C parsing".
  - Julia version reading the file as bytes and manually walking through the bytes. label: "Optimized Julia".

<img src="https://raw.githubusercontent.com/abelsiqueira/call-julia-from-python-experiments/main/assets/comparison.png" width="49%">
<img src="https://raw.githubusercontent.com/abelsiqueira/call-julia-from-python-experiments/main/assets/comparison-relative.png" width="49%">

Take-aways (see blog post):
- The "Basic Julia" case is already an improvement over the "Pure Python" case.
- The "Optimized Julia" case is faster than the "C++" case.
- If you don't know Julia nor C++, moving the slow code to Julia yields benefits faster and with less effort.

## Building the docker images

  ```shell
docker build --tag jl-from-py:<VERSION>
  ```

## Reproducting the results

- Download dataset and store in a folder called `dataset`: [![Zenodo badge][dataset-badge]][dataset]
- Get the image with
  ```shell
  docker pull abelsiqueira/jl-from-py:0.3.0
  ```
- Run it with

  ```shell
  docker run --rm --volume "$PWD/dataset:/app/dataset" --volume "$PWD/out:/app/out" jl-from-py:0.3.0 --max-num-files 0
  ```
- You will find the outputs in the `out/` folder.

The docker runs the script `src/main.py` that runs `run_experiments.py` and `run_analysis.py`.

### Arguments

- `--folder FOLDER`: Set the dataset folder. (Default: `dataset`).
- `--max-num-files N`: Maximum number of files to read from can be used to limit the experiment. The files are traversed in sorted name order. Use 0 or a negative number to run all. (Default: `0`).
- `--skip-after X`: Time threshold in seconds to skip the tests of a specific version. If the threshold is reached twice, that version is skipped in the additional tests. (Default: `10`).
- `--skip VALUE1 [VALUE2 ...]`: List of versions to skip. Valid values: `python`, `cpp`, `julia_basic`, `julia_c`, `julia_prealloc`, `julia_opt`.

[patrick]: https://blog.esciencecenter.nl/irregular-data-in-pandas-using-c-88ce311cb9ef
[dataset]: https://zenodo.org/record/5816746
[dataset-badge]: https://zenodo.org/badge/DOI/10.5281/zenodo.5816746.svg

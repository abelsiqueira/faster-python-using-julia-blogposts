# Calling Julia from Python - an experiment on data loading

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5708268.svg)](https://doi.org/10.5281/zenodo.5708268)

See the [slides](slides).

## TLDR

After reading [Patrick's blog post][patrick], we decided to try to replace C++ with Julia to check:
- How easy/hard it is
- How much improvement can be gained with a basic version
- How much improvement can be gained with an optimized version

A basic version is already an improvement over the pure Python version, and an optimized version was faster than the C++ version.

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

[patrick]: https://blog.esciencecenter.nl/irregular-data-in-pandas-using-c-88ce311cb9ef
[dataset]: https://zenodo.org/record/5816746
[dataset-badge]: https://zenodo.org/badge/DOI/10.5281/zenodo.5816746.svg

# Calling Julia from Python - an experiment on data loading

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5708268.svg)](https://doi.org/10.5281/zenodo.5708268)

See the [slides](slides).

## TLDR

After reading [Patrick's blog post][patrick], we decided to try to replace C++ with Julia to check:
- How easy/hard it is
- How much improvement can be gained with a basic version
- How much improvement can be gained with an optimized version

A basic version is already an improvement over the pure Python version, and an optimized version was faster than the C++ version.

## Building the docker images

  ```shell
docker build --tag jl-from-py:<VERSION>
  ```

## Reproducting the results

- Download dataset and store in a folder called `gen-data`: [![Zenodo badge][dataset-badge]][dataset]

- Get the image with

  ```shell
  docker pull abelsiqueira/jl-from-py:0.2.0
  ```

- Run it with

  ```shell
  docker run --rm --volume "$PWD/gen-data:/app/gen-data" --volume "$PWD/out:/app/out" jl-from-py:0.2.0 --max-num-files 1000
  ```

- You will find the output in the `out/` folder.

The docker runs the script `src/main.py` that runs `run_experiments.py` and `run_analysis.py`.
The `--max-num-files` can be used to limit the experiment. The files are traversed in name order.
You can also use `--folder` to set a different folder than `gen-data`.

[patrick]: https://blog.esciencecenter.nl/irregular-data-in-pandas-using-c-88ce311cb9ef
[dataset]: https://doi.org/10.5281/zenodo.5707672
[dataset-badge]: https://zenodo.org/badge/DOI/10.5281/zenodo.5707672.svg

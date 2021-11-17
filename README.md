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

- Follow [Patrick's blog post][patrick] to install the C++ part.
- Install Julia (We've used Julia 1.6.3)
  - I recommend using [Jill]
  - We'll refer to this Julia as `path/to/julia`.
- Install Python
  - Ideally, one dynamically linked to `libpython`.
  - To test it, use `ldd path/to/python` and look for `libpython3.9`. It should exist for the shared version.
  - If you don't have, look into workarounds [here][pyjulia-trouble]
  - Tip: Archlinux's system Python is dynamically linked.
  - We've used Python 3.9.7 from Archlinux.
- Open Julia and enter the following commands:
  - `ENV["PYTHON"] = "path/to/python"`
  - `using Pkg`
  - `Pkg.add("PyCall")`
  - This will make sure that the packages we are installing use the correct Python version
- Install `juliapy` with `path/to/python -m pip install julia`
- Run `path/to/python` and enter
  - `import julia`
  - `julia.install("julia=path/to/julia")`
- Download dataset and store in `gen-data` folder: [![Zenodo badge][dataset-badge]][dataset]
- Run `scalability_test.py` - it should take several hours (over 10) and consume a moderate amount of memory.
- Run `scalability_analysis.py`.

[patrick]: https://blog.esciencecenter.nl/irregular-data-in-pandas-using-c-88ce311cb9ef
[Jill]: https://github.com/abelsiqueira/jill
[pyjulia-trouble]: https://pyjulia.readthedocs.io/en/latest/troubleshooting.html
[dataset]: https://doi.org/10.5281/zenodo.5707672
[dataset-badge]: https://zenodo.org/badge/DOI/10.5281/zenodo.5707672.svg

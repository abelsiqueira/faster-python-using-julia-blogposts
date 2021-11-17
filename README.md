# Calling Julia from Python - an experiment on data loading

See the [slides](slides).

## TLDR

After reading https://blog.esciencecenter.nl/irregular-data-in-pandas-using-c-88ce311cb9ef, we decided to try to replace C++ with Julia to check:
- How easy/hard it is
- How much improvement can be gained with a basic version
- How much improvement can be gained with an optimized version

A basic version is already an improvement over the pure Python version, and an optimized version was faster than the C++ version.
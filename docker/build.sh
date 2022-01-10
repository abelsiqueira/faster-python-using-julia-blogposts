#!/bin/bash
set -e

for pyver in 3.10.1 3.9.9
do
    for jlver in 1.6.5 1.7.1
    do
        echo "Building for Python: ${pyver}  Julia: ${jlver}"
        tagName=abelsiqueira/python-and-julia:py$(echo ${pyver} | cut -d"." -f1-2)-jl$(echo ${jlver} | cut -d"." -f1-2)
        docker build --file Dockerfile \
            --tag ${tagName} \
            --build-arg PYTHON_VERSION=${pyver} \
            --build-arg JULIA_VERSION=${jlver} \
            .
    done
done

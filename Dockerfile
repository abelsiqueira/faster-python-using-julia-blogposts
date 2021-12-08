FROM ubuntu:20.10

LABEL MAINTAINER abel.siqueira@esciencecenter.nl
ENV container docker

RUN mkdir /app
WORKDIR /app

# PACKAGES
#===========================================
RUN rm -f /etc/localtime && \
    ln -s /usr/share/zoneinfo/Europe/Amsterdam /etc/localtime

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y gcc git make cmake wget unzip \
        build-essential libssl-dev zlib1g-dev \
        libbz2-dev libreadline-dev libsqlite3-dev curl llvm \
        libncurses5-dev libncursesw5-dev xz-utils tk-dev

# INSTALL PYTHON
#===========================================
COPY pyproject.toml poetry.lock /app/
RUN wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz && \
    tar -zxf Python-3.9.9.tgz && \
    cd Python-3.9.9 && \
    ./configure --with-ensurepip=install --enable-shared && make && make install && \
    ldconfig && \
    ln -sf python3 /usr/local/bin/python

# Install poetry - notice that we use a preview version because we want 1.2.0
# This should be changed in the future to use `POETRY_VERSION=1.2.0`.
RUN curl -sSL https://install.python-poetry.org | POETRY_PREVIEW=1 python3 - && \
    ln -sf ~/.local/bin/poetry /usr/local/bin/poetry && \
    poetry install --with cpp

# INSTALL C++ PACKAGES
#================================

RUN wget https://github.com/xtensor-stack/xtl/archive/refs/tags/0.7.4.tar.gz -O xtl.tar.gz && \
    tar -zxf xtl.tar.gz && \
    cd /app/xtl-0.7.4 && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr && \
    make install

RUN wget https://github.com/xtensor-stack/xtensor/archive/refs/tags/0.24.0.tar.gz -O xtensor.tar.gz && \
    tar -zxf xtensor.tar.gz && \
    cd /app/xtensor-0.24.0 && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr && \
    make install

RUN wget https://github.com/xtensor-stack/xtensor-python/archive/refs/tags/0.26.0.tar.gz -O xtensor-python.tar.gz && \
    tar -zxf xtensor-python.tar.gz && \
    cd /app/xtensor-python-0.26.0 && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_PREFIX_PATH=$(dirname $(poetry run which python))/.. && \
    make install

RUN wget https://github.com/TICCLAT/ticcl-output-reader/archive/9474533092f6438053d660fd57b645a41b0f9345.zip -O ticcl.zip && \
    unzip ticcl.zip && \
    mv ticcl-output-reader* ticcl-output-reader && \
    poetry run pip install ./ticcl-output-reader

# INSTALL JULIA
#====================================
COPY Project.toml Manifest.toml *.jl *.py /app/

RUN wget https://raw.githubusercontent.com/abelsiqueira/jill/main/jill.sh && \
    bash /app/jill.sh -y -v 1.6.4 && \
    export PYTHON=$(poetry run which python) && \
    julia --project -e 'using Pkg; Pkg.instantiate()' && \
    poetry run python -c 'import julia; julia.install()'

COPY *.jl *.py /app/

# CLEAN UP
#===========================================

RUN rm -rf /var/cache/pacman/pkg/* /app/jill.sh /opt/julias/*.tar.gz /app/*.tar.gz

ENTRYPOINT ["poetry", "run", "python", "-u", "/app/scalability_test.py"]
CMD ["2"]


# docker run --rm --volume "./gen-data:/app/gen-data" --volume "./out:/app/out" jl-from-py:0.1.0 2
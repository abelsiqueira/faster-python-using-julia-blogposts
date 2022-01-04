FROM ubuntu:21.10

LABEL MAINTAINER abel.siqueira@esciencecenter.nl
ENV container docker
ENV DEBIAN_FRONTEND noninteractive
ENV LANG en_US.utf8
ENV MAKEFLAGS -j4

RUN mkdir /app
WORKDIR /app

# DEPENDENCIES
#===========================================
RUN apt-get update -y && \
    apt-get install -y gcc git make cmake wget unzip \
        build-essential libssl-dev zlib1g-dev \
        libbz2-dev libreadline-dev libsqlite3-dev curl llvm \
        libncurses5-dev libncursesw5-dev xz-utils tk-dev

# INSTALL PYTHON
#===========================================
COPY requirements.txt /app/

RUN wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz && \
    tar -zxf Python-3.9.9.tgz && \
    cd Python-3.9.9 && \
    ./configure --with-ensurepip=install --enable-shared && make && make install && \
    ldconfig && \
    ln -sf python3 /usr/local/bin/python

RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install -r requirements.txt

# INSTALL ticcl-output-reader and dependencies
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
    cmake -DCMAKE_INSTALL_PREFIX=/usr && \
    make install
RUN wget https://github.com/TICCLAT/ticcl-output-reader/archive/9474533092f6438053d660fd57b645a41b0f9345.zip -O ticcl.zip && \
    unzip ticcl.zip && \
    mv ticcl-output-reader* ticcl-output-reader && \
    python -m pip install ./ticcl-output-reader

# INSTALL JULIA
#====================================
COPY Project.toml /app/
RUN wget https://raw.githubusercontent.com/abelsiqueira/jill/main/jill.sh && \
    bash /app/jill.sh -y -v 1.6.4 && \
    export PYTHON="/usr/local/bin/python" && \
    julia --project -e 'using Pkg; Pkg.instantiate()' && \
    python -c 'import julia; julia.install()'


# COPY SCRIPTS
#===========================================
COPY src /app/


# CLEAN UP
#===========================================
RUN rm -rf /app/jill.sh \
    /opt/julias/*.tar.gz \
    /app/*.tar.gz /app/Python-3.9.9.tgz /app/ticcl.zip /app/__pycache__

RUN apt-get purge -y gcc git make cmake wget unzip \
        build-essential libssl-dev zlib1g-dev \
        libbz2-dev libreadline-dev libsqlite3-dev curl llvm \
        libncurses5-dev libncursesw5-dev xz-utils tk-dev && \
    apt-get autoremove -y


# ENTRYPOINT ["python", "-u", "/app/src/main.py"]
# CMD ["--max-num-files", "2"]

# build: docker build --tag jl-from-py:0.3.0 .
# run: docker run --rm --volume "./gen-data:/app/gen-data" --volume "./out:/app/out" jl-from-py:0.3.0 2

FROM abelsiqueira/python-and-julia:py3.10-jl1.6

LABEL MAINTAINER abel.siqueira@esciencecenter.nl
ENV container docker
ENV DEBIAN_FRONTEND noninteractive
ENV LANG en_US.utf8
ENV MAKEFLAGS -j4

WORKDIR /app

# DEPENDENCIES
#===========================================
RUN apt-get update -y && \
    apt-get install -y gcc git make cmake wget unzip \
        build-essential libssl-dev zlib1g-dev \
        libbz2-dev libreadline-dev libsqlite3-dev curl llvm \
        libncurses5-dev libncursesw5-dev xz-utils tk-dev

# INSTALL PYTHON DEPENDENCIES
#===========================================
COPY requirements.txt /app/

RUN python -m pip install -r requirements.txt

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
RUN julia --project -e 'using Pkg; Pkg.instantiate()'


# COPY SCRIPTS
#===========================================
COPY src/ /app/src/


# CLEAN UP
#===========================================
RUN rm -rf /app/*.tar.gz /app/ticcl.zip /app/__pycache__

RUN apt-get purge -y gcc git make cmake wget unzip \
        build-essential libssl-dev zlib1g-dev \
        libbz2-dev libreadline-dev libsqlite3-dev curl llvm \
        libncurses5-dev libncursesw5-dev xz-utils tk-dev && \
    apt-get autoremove -y


ENTRYPOINT ["python", "-u", "/app/src/main.py"]
CMD ["--max-num-files", "0", "--skip-after", "0"]

# build: docker build --tag abelsiqueira/faster-python-with-julia-blogpost:post3 .
# run: docker run --rm --volume "$PWD/dataset:/app/dataset" --volume "$PWD/out:/app/out" abelsiqueira/faster-python-with-julia-blogpost:post3

FROM ubuntu:21.10

LABEL MAINTAINER abel.siqueira@esciencecenter.nl
ARG PYTHON_VERSION=3.10.1
ARG JULIA_VERSION=1.7.1

ENV container docker
ENV DEBIAN_FRONTEND noninteractive
ENV LANG en_US.utf8
ENV MAKEFLAGS -j4

RUN mkdir /app
WORKDIR /app

# DEPENDENCIES
#===========================================
RUN apt-get update -y && \
    apt-get install -y gcc make wget zlib1g-dev libffi-dev libssl-dev

# INSTALL PYTHON
#===========================================
RUN wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz && \
    tar -zxf Python-$PYTHON_VERSION.tgz && \
    cd Python-$PYTHON_VERSION && \
    ./configure --with-ensurepip=install --enable-shared && make && make install && \
    ldconfig && \
    ln -sf python3 /usr/local/bin/python
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install julia

# INSTALL JULIA
#====================================
RUN wget https://raw.githubusercontent.com/abelsiqueira/jill/main/jill.sh && \
    bash /app/jill.sh -y -v $JULIA_VERSION && \
    export PYTHON="python" && \
    julia -e 'using Pkg; Pkg.add("PyCall")' && \
    python -c 'import julia; julia.install()'

# CLEAN UP
#===========================================
RUN rm -rf /app/jill.sh \
    /opt/julias/*.tar.gz \
    /app/Python-3.9.9.tgz

RUN apt-get purge -y gcc make wget zlib1g-dev libffi-dev libssl-dev && \
    apt-get autoremove -y

CMD ["/bin/bash"]

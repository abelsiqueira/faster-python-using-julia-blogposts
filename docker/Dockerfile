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

# INSTALL PYTHON
#===========================================
RUN wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz && \
    tar -zxf Python-$PYTHON_VERSION.tgz && \
    cd Python-$PYTHON_VERSION && \
    ./configure --with-ensurepip=install --enable-shared && make && make install && \
    ldconfig && \
    ln -sf python3 /usr/local/bin/python


# INSTALL JULIA
#====================================
RUN wget https://raw.githubusercontent.com/abelsiqueira/jill/main/jill.sh && \
    bash /app/jill.sh -y -v $JULIA_VERSION && \
    export PYTHON="/usr/local/bin/python" && \
    julia --project -e 'using Pkg; Pkg.add("PyCall")' && \
    python -c 'import julia; julia.install()'

CMD ["/bin/bash"]

FROM archlinux:base-devel-20211121.0.39613

LABEL MAINTAINER abel.siqueira@esciencecenter.nl
ENV container docker
ENV LC_ALL en_US.UTF-8

RUN mkdir /app
WORKDIR /app

# PACKAGES
#===========================================
RUN rm -f /etc/localtime && \
    ln -s /usr/share/zoneinfo/Europe/Amsterdam /etc/localtime

RUN pacman -Syyuu --noconfirm && \
    pacman -S --noconfirm --needed \
    binutils gcc fakeroot make base-devel \
    wget git cmake pybind11

# INSTALL PYTHON
#===========================================
RUN pacman -S --noconfirm \
    python python-pip
ENV PYTHON /usr/bin/python

# INSTALL JULIA
RUN wget https://raw.githubusercontent.com/abelsiqueira/jill/main/jill.sh && \
    bash /app/jill.sh -y -v 1.6.4 && \
    julia -e 'using Pkg; Pkg.add("PyCall"); Pkg.add("Parsers")'

RUN python -m pip install --upgrade pip && \
    python -m pip install julia numpy pandas && \
    python -c 'import julia; julia.install()'

# INSTALL C++ (and packages)
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

RUN git clone https://github.com/TICCLAT/ticcl-output-reader && \
    python -m pip install ./ticcl-output-reader

# COPY files /app/...
COPY docker/docker_test.py jl_* /app/

# CLEAN UP
#===========================================

RUN rm -rf /var/cache/pacman/pkg/* /app/jill.sh /opt/julias/*.tar.gz /app/*.tar.gz

# CMD ["python", "/app/scalability_test.py"]
ENTRYPOINT ["python", "/app/docker_test.py"]
CMD ["5"]


# docker run --rm --volume "./gen-data:/app/gen-data" --volume "./out:/app/out" jl-from-py:0.1.0
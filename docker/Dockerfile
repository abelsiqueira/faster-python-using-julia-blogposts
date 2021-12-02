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
    wget git

# INSTALL PYTHON
#===========================================
RUN pacman -S --noconfirm \
    python python-pip
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh -O miniconda.sh
RUN bash miniconda.sh -b -p /app/miniconda3
ENV PATH /app/miniconda3/bin:$PATH
RUN conda init
RUN conda install xtensor-python -c conda-forge

# INSTALL JULIA
RUN wget https://raw.githubusercontent.com/abelsiqueira/jill/main/jill.sh
RUN bash /app/jill.sh -y -v 1.6.4
ENV PYTHON /usr/bin/python
RUN julia -e 'using Pkg; Pkg.add("PyCall"); Pkg.add("Parsers")'

RUN python -m pip install --upgrade pip && \
    python -m pip install julia numpy pandas

RUN python -c 'import julia; julia.install()'

# COPY files /app/...
COPY docker/docker_test.py jl_* /app/

# INSTALL C++ (and packages)
RUN git clone https://github.com/TICCLAT/ticcl-output-reader
RUN python -m pip install ./ticcl-output-reader


# CLEAN UP
#===========================================

RUN rm -rf /var/cache/pacman/pkg/* /app/jill.sh /opt/julias/*.tar.gz miniconda.sh

# CMD ["python", "/app/scalability_test.py"]
CMD ["python", "/app/docker_test.py"]

# docker run --rm --volume "./gen-data:/app/gen-data" --volume "./out:/app/out" jl-from-py:0.1.0
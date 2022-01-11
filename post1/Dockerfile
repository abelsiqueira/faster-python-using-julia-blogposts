FROM abelsiqueira/python-and-julia:py3.10-jl1.6

LABEL MAINTAINER abel.siqueira@esciencecenter.nl

ENV container docker
ENV DEBIAN_FRONTEND noninteractive
ENV LANG en_US.utf8

WORKDIR /app

# INSTALL PYTHON PACKAGES
#====================================
RUN python -m pip install ipython matplotlib

# INSTALL JULIA PACKAGES
#====================================
RUN julia -e 'using Pkg; Pkg.add("ForwardDiff")'

# COPY FILES
#====================================
COPY *.py /app/

# CLEAN UP
#===========================================
RUN rm -rf /app/jill.sh \
    /opt/julias/*.tar.gz \
    /app/Python-3.9.9.tgz

CMD ["/bin/bash"]

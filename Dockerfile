# Base Image
FROM biocontainers/biocontainers:latest

# Metadata
LABEL base.image="biocontainers:latest"
LABEL version="0.9"
LABEL software="DeepMito"
LABEL software.version="2018012"
LABEL description="an open source software tool to predict protein sub-mitochondrial localization"
LABEL website="http://comet-ms.sourceforge.net/"
LABEL documentation="http://comet-ms.sourceforge.net/parameters/parameters_2016010/"
LABEL license="http://busca.biocomp.unibo.it/deepmito/"
LABEL tags="Proteomics"

# Maintainer
MAINTAINER Castrense Savojard <castrense.savojardo2@unibo.it>

USER biodocker

COPY ./deepmito.zip /home/biodocker/
COPY ./requirements.txt /home/biodocker/
RUN cd /home/biodocker/ && unzip deepmito.zip && cp deepmito/deepmito.py /home/biodocker/bin/  && pip install -r requirements.txt
ENV PATH /home/biodocker/bin:$PATH

WORKDIR /data/
ENTRYPOINT ["python", "/home/biodocker/bin/deepmito.py"]

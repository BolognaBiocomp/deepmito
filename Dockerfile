# Base Image
FROM biocontainers/biocontainers:latest

# Metadata
LABEL base.image="biocontainers:latest"
LABEL version="0.9"
LABEL software="DeepMito"
LABEL software.version="2018012"
LABEL description="an open source software tool to predict protein sub-mitochondrial localization"
LABEL website="http://busca.biocomp.unibo.it/deepmito/"
LABEL documentation="http://busca.biocomp.unibo.it/deepmito/"
LABEL license="http://busca.biocomp.unibo.it/deepmito/"
LABEL tags="Proteomics"
LABEL maintainer="Castrense Savojardo <castrense.savojardo2@unibo.it>"

COPY requirements.txt /home/biodocker/deepmito/

USER root

RUN apt update && apt install -y "ncbi-blast+" && pip install --no-cache-dir -r /home/biodocker/deepmito/requirements.txt

USER biodocker

COPY . /home/biodocker/deepmito/

WORKDIR /data/

# Verbosity level of Tensorflow
ENV TF_CPP_MIN_LOG_LEVEL 3

ENTRYPOINT ["python", "/home/biodocker/deepmito/deepmito.py"]

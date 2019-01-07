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
LABEL maintainer="Castrense Savojard <castrense.savojardo2@unibo.it>"

USER biodocker

COPY . /home/biodocker/deepmito/

RUN pip install -r /home/biodocker/deepmito/requirements.txt

WORKDIR /data/

ENTRYPOINT ["python", "/home/biodocker/deepmito/deepmito.py"]

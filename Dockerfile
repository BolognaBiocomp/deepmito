# Base Image
FROM python:2.7.15-slim-stretch

# Metadata
LABEL base.image="biocontainers:latest" \
 version="0.9" \
 software="DeepMito" \
 software.version="2018012" \
 description="An open source software tool to predict protein sub-mitochondrial localization." \
 website="http://busca.biocomp.unibo.it/deepmito/" \
 documentation="http://busca.biocomp.unibo.it/deepmito/" \
 license="http://busca.biocomp.unibo.it/deepmito/" \
 tags="Proteomics" \
 maintainer="Castrense Savojardo <castrense.savojardo2@unibo.it>" 
 
RUN useradd -m biodocker

COPY . /home/biodocker/

RUN pip install -r /home/biodocker/requirements.txt


USER biodocker

ENV PATH /home/biodocker:$PATH

WORKDIR /data/
ENTRYPOINT ["python", "/home/biodocker/deepmito.py"]

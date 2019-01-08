# Base Image
FROM python:2.7.15-slim-stretch

# Metadata
LABEL base.image="python:2.7.15-slim-stretch"
LABEL version="0.9"
LABEL software="DeepMito"
LABEL software.version="2018012"
LABEL description="an open source software tool to predict protein sub-mitochondrial localization"
LABEL website="http://busca.biocomp.unibo.it/deepmito/software/"
LABEL documentation="http://busca.biocomp.unibo.it/deepmito/software/"
LABEL license="GNU GENERAL PUBLIC LICENSE Version 3"
LABEL tags="Proteomics"
LABEL maintainer="Castrense Savojardo <castrense.savojardo2@unibo.it>"

WORKDIR /usr/src/deepmito

COPY requirements.txt ./

RUN apt-get update && apt install -y "ncbi-blast+" && \
    pip install --no-cache-dir -r requirements.txt && \
    useradd -m deepmito

USER deepmito

COPY . .

WORKDIR /data/

# Verbosity level of Tensorflow
ENV TF_CPP_MIN_LOG_LEVEL=3 DEEPMITOROOT=/usr/src/deepmito PATH=/usr/src/deepmito:$PATH

CMD ["deepmito.py", "-h"]
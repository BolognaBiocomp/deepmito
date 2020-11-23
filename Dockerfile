# Base Image
FROM continuumio/miniconda3

# Metadata
LABEL base.image="continuumio/miniconda3"
LABEL version="1.0"
LABEL software="DeepMito"
LABEL software.version="1.0"
LABEL description="an open source software tool to predict protein sub-mitochondrial localization"
LABEL website="https://busca.biocomp.unibo.it/deepmito/software/"
LABEL documentation="https://busca.biocomp.unibo.it/deepmito/software/"
LABEL license="GNU GENERAL PUBLIC LICENSE Version 3"
LABEL tags="Proteomics"
LABEL maintainer="Castrense Savojardo <castrense.savojardo2@unibo.it>"

ENV PYTHONDONTWRITEBYTECODE=true

WORKDIR /usr/src/deepmito

COPY . .

WORKDIR /data/

RUN conda update -n base conda && \
   conda install --yes nomkl keras==2.4.3 biopython==1.78 tensorflow==2.2.0 && \
   conda install --yes nomkl blast -c bioconda && \
   conda clean -afy \
   && find /opt/conda/ -follow -type f -name '*.a' -delete \
   && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
   && find /opt/conda/ -follow -type f -name '*.js.map' -delete

# Verbosity level of Tensorflow
ENV TF_CPP_MIN_LOG_LEVEL=3 DEEPMITOROOT=/usr/src/deepmito PATH=/usr/src/deepmito:$PATH

CMD ["deepmito.py", "-h"]

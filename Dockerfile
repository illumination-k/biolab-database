FROM conda/miniconda3

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN conda install -c bioconda -c conda-forge \
    blast \
    biopython \
    pydna \
    fastapi \
    uvicorn

WORKDIR /app
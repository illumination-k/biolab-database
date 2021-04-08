FROM conda/miniconda3 AS conda

RUN conda install -c bioconda blast

FROM python:3.9.2-slim

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt && rm -rf /tmp/*

WORKDIR /app
FROM python:3.9.2-slim

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt update -y --fix-missing && \
    apt install -y git gcc zsh curl peco && \
    curl -L https://raw.githubusercontent.com/illumination-k/dotfiles/master/etc/install.sh | bash

COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt && rm -rf /tmp/*

WORKDIR /app

CMD [ "zsh" ]
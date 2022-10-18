FROM ubuntu:latest
WORKDIR /usr/src/drugstone/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update --no-install-recommends && apt-get upgrade -y && apt-get install -y supervisor nginx libgtk-3-dev wget ssh git build-essential
RUN apt-get autoclean -y && apt-get autoremove -y

RUN mkdir ~/.ssh/
RUN ssh-keyscan github.com >> ~/.ssh/known_hosts

ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py38_4.12.0-Linux-x86_64.sh -O ~/miniconda.sh && /bin/bash ~/miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
RUN conda init bash

WORKDIR /usr/src/robust-web
RUN git clone https://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@github.com/bionetslab/robust-web.git
WORKDIR /usr/src/robust-web/robust-web
RUN git checkout docker
RUN rm -rf .git
RUN git clone  https://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@github.com/bionetslab/robust_bias_aware.git
RUN rm -rf robust_bias_aware/.git

RUN conda install python=3.7

#COPY ./requirements.txt ./
RUN pip install -r requirements.txt
#RUN pip install importlib-metadata==4.13.0
#COPY celery.sh ./
#COPY celery.env ./
#COPY app.py ./
EXPOSE 5000

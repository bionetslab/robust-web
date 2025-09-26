FROM ubuntu:noble as robust-web_base
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get dist-upgrade -y && apt-get install -y supervisor libgtk-3-dev wget apt-utils
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release software-properties-common cron unzip nginx ssh git build-essential
RUN apt-get autoclean -y && apt-get autoremove -y && apt-get clean -y

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu lunar stable"

RUN apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io

ENV CONDA_DIR /opt/conda
RUN wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
RUN bash Miniforge3-$(uname)-$(uname -m).sh -b -p "${CONDA_DIR}"
ENV PATH=$CONDA_DIR/bin:$PATH
RUN chmod +x "${CONDA_DIR}/etc/profile.d/conda.sh"
RUN "${CONDA_DIR}/etc/profile.d/conda.sh"
RUN chmod +x "${CONDA_DIR}/etc/profile.d/mamba.sh"
RUN "${CONDA_DIR}/etc/profile.d/mamba.sh"

RUN conda init bash

RUN mamba update -n base -c defaults mamba conda
RUN mamba install -y python=3.10
RUN mamba update -y --all
RUN pip install pip==23
RUN pip install --upgrade pip requests cryptography pyopenssl
RUN chmod 777 -R /opt/conda

FROM robust-web_base

WORKDIR /usr/src/robust-web/

RUN mkdir -p ~/.ssh/
RUN ssh-keyscan github.com >> ~/.ssh/known_hosts

WORKDIR /usr/src/robust-web

RUN conda install python=3.8

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./
RUN rm -rf .git

RUN apt-get remove -y git ssh wget curl unzip nginx

EXPOSE 5000

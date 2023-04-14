FROM andimajore/miniconda3_lunar
WORKDIR /usr/src/robust-web/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update
RUN apt-get install --fix-missing -y supervisor nginx libgtk-3-dev wget ssh git build-essential

RUN mkdir -p ~/.ssh/
RUN ssh-keyscan github.com >> ~/.ssh/known_hosts

WORKDIR /usr/src/robust-web

RUN conda install python=3.8

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./
RUN rm -rf .git

EXPOSE 5000

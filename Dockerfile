FROM ubuntu:xenial
MAINTAINER Concrete Solutions
WORKDIR /usr/src
RUN apt-get -qq update && apt-get install -y sqlite3 libmysqlclient-dev ca-certificates python-dev python3-pip python3
RUN pip3 install --upgrade pip
ADD requirements.txt requirements.txt
ADD requirements-dev.txt requirements-dev.txt
ADD setup.py setup.py
RUN pip3 install -r requirements-dev.txt

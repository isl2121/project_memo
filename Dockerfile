FROM ubuntu:16.04

MAINTAINER isl2121@naver.com

ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8

# 기본 패키지들 설치 및 Python 3.6 설치
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc
RUN apt-get install -y git

RUN python3 -m pip install pip --upgrade

ADD . /app

EXPOSE 8000

WORKDIR /app

RUN pip3 install -r requirements.txt

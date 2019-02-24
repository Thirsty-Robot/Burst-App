FROM python:latest

WORKDIR /Burst
ADD . /Burst

RUN pip install -r requirements.txt
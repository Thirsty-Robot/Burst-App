FROM python:latest

COPY . /burst
WORKDIR /burst

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "server.py" ]
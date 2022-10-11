FROM python:3.9.14-buster

RUN mkdir /app

COPY ./requirements*.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt -r requirements-test.txt

CMD bash
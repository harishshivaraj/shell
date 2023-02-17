FROM python:3.10-slim-buster

ENV HOST=0.0.0.0
ENV PORT=8080

RUN mkdir -p /shell

WORKDIR /shell

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./instruments ./instruments
COPY ./market-data ./market-data
COPY ./models ./models
COPY ./securities ./securities
COPY ./*.py .

CMD flask --app=pricing_engine run --host=$HOST --port=$PORT
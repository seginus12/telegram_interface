FROM python:3.12-slim

WORKDIR /app

RUN apt update && apt upgrade -y && \
    apt install -y build-essential libssl-dev libffi-dev python3-dev && \
    pip install --upgrade pip

COPY requirements.txt .
# RUN cat requirements.txt
RUN pip install -r requirements.txt

RUN touch updates_file.txt

COPY . .
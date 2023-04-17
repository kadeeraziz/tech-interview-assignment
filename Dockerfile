FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && \
    apt install -y wget && \
    apt-get install -y --no-install-recommends gcc  \
    libpq-dev -y  \ 
    python3-dev \
    python3-venv python3-wheel -y 

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

FROM python:3.8

RUN apt update

RUN apt install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    build-essential \
    cmake \
    pkg-config

RUN apt install -y rustc

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY . ./

RUN poetry install

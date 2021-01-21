FROM ubuntu:20.04

RUN apt update && apt install -y postgresql-client python3 python-is-python3

ADD import-backfill.py .
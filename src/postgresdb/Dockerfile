FROM postgres:latest

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB postgres
RUN apt-get update
RUN apt-get install net-tools
ADD init.sql /docker-entrypoint-initdb.d
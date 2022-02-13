FROM python:3.10
COPY . /worker
WORKDIR /worker
RUN pip install -r requirements.txt
ENTRYPOINT celery -A tasks worker --loglevel=info
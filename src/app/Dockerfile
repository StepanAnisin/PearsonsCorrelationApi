FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT celery -A tasks worker --loglevel=info
ENTRYPOINT ["python3"]
CMD ["wsgi.py"]

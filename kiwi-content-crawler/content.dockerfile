#FROM tiangolo/uwsgi-nginx-flask:python3.6
FROM python:3

ENV PYTHONPATH=$PYTHONPATH:/app
ENV MONGO_HOST=mongodb-content
ENV MONGO_PORT=27017
ENV MONGO_DB=imgur_posts
ENV MONGO_COLLECTION=posts 
ENV MONGO_USER=admin
ENV MONGO_PWD=12345
ENV IMGUR_CLIENT_ID=***REMOVED***

COPY ./app /app
COPY ./requirements.txt /app

WORKDIR /app

EXPOSE 5000

RUN pip install -r requirements.txt 

ENTRYPOINT [ "python", "main.py" ]
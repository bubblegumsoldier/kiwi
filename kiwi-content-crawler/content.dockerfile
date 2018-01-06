#FROM tiangolo/uwsgi-nginx-flask:python3.6
FROM python:3

ENV PYTHONPATH=$PYTHONPATH:/kiwi
ENV MONGO_HOST=***REMOVED***
ENV MONGO_PORT=27017
ENV MONGO_DB=imgur_posts
ENV MONGO_COLLECTION=posts 
ENV MONGO_USER=lange
ENV MONGO_PWD=***REMOVED***
ENV IMGUR_CLIENT_ID=***REMOVED***
# One week in seconds
ENV RESET_PAGE_TIME=604800


COPY ./kiwi /kiwi
COPY ./requirements.txt /

WORKDIR /

EXPOSE 5000

RUN pip install -r requirements.txt 

ENTRYPOINT [ "python", "kiwi/main.py" ]

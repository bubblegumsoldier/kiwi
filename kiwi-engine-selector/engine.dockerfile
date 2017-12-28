FROM python:3

ENV PYTHONPATH=$PYTHONPATH:/var/www/kiwi
ENV MONGO_HOST=***REMOVED***
ENV MONGO_PORT=27017
ENV MONGO_DB=imgur_posts
ENV MONGO_COLLECTION=posts 
ENV MONGO_USER=lange	
ENV MONGO_PWD=***REMOVED***

EXPOSE 8000


COPY ./kiwi /var/www/kiwi
COPY ./requirements.txt /var/www

WORKDIR var/www

RUN pip install -r requirements.txt 

ENTRYPOINT [ "python", "kiwi/app.py" ]

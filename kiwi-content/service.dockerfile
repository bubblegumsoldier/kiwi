FROM python:3

ENV MSQL_USER=content
ENV MSQL_PWD=12345
ENV MSQL_HOST=***REMOVED***
ENV MSQL_PORT=3310
ENV MSQL_DATABASE=content_recommender
ENV PYTHONPATH=$PYTHONPATH:/var/www/kiwi

ENV MAX_RATING=5
ENV MIN_RATING=1
ENV POS_CUTOFF=3.5

EXPOSE 8000


COPY ./kiwi /var/www/kiwi
COPY ./requirements.txt /var/www

WORKDIR var/www

RUN pip install -r requirements.txt 

ENTRYPOINT [ "python", "kiwi/app.py" ]

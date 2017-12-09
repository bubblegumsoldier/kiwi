FROM python:3

ENV MSQL_USER=random
ENV MSQL_PWD=12345
ENV MSQL_HOST=***REMOVED***
ENV MSQL_PORT=3306
ENV MSQL_DATABASE=random_recommender
ENV PYTHONPATH=$PYTHONPATH:/var/www/kiwi

EXPOSE 8000


COPY ./kiwi /var/www/kiwi
COPY ./requirements.txt /var/www

WORKDIR var/www

RUN pip install -r requirements.txt 

ENTRYPOINT [ "python", "kiwi/app.py" ]

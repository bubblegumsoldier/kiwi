FROM python:3

ENV MSQL_USER=root
ENV MSQL_PWD=12345
ENV MSQL_HOST=my-mysql
ENV MSQL_PORT=3306
ENV MSQL_DATABASE=random_recommender
ENV PYTHONPATH=$PYTHONPATH:/var/www
EXPOSE 8901


COPY ./kiwi /var/www/kiwi
COPY ./requirements.txt /var/www
WORKDIR /var/www

RUN pip install -r requirements.txt 

ENTRYPOINT [ "python", "kiwi/app.py" ]
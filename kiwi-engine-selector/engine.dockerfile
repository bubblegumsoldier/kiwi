FROM python:3

ENV PYTHONPATH=$PYTHONPATH:/var/www/kiwi

EXPOSE 8000


COPY ./kiwi /var/www/kiwi
COPY ./requirements.txt /var/www

WORKDIR var/www

RUN pip install -r requirements.txt 

ENTRYPOINT [ "python", "kiwi/app.py" ]

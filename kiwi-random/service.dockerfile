FROM python:3

EXPOSE 8000

ENV PYTHONPATH=$PYTHONPATH:/var/www/kiwi

COPY ./kiwi /var/www/kiwi
COPY ./requirements.txt /var/www

WORKDIR var/www

RUN pip install -r requirements.txt 

ENTRYPOINT [ "python", "kiwi/app.py" ]

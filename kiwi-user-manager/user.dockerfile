FROM tiangolo/uwsgi-nginx-flask:python3.6

ENV PYTHONPATH=$PYTHONPATH:/app
ENV KIWI_USER_MANAGER_DB_HOST=***REMOVED***
ENV KIWI_USER_MANAGER_DB_DATABASE=kiwi_users
ENV KIWI_USER_MANAGER_DB_USER=lange
ENV KIWI_USER_MANAGER_DB_PASSWORD=***REMOVED***

COPY ./app /app
COPY ./requirements.txt /app

RUN pip install -r requirements.txt 

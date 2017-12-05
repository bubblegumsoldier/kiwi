FROM tiangolo/uwsgi-nginx-flask:python3.6

ENV PYTHONPATH=$PYTHONPATH:/app
ENV KIWI_USER_MANAGER_DB_HOST=mongodb-user
ENV KIWI_USER_MANAGER_DB_DATABASE=kiwi_users
ENV KIWI_USER_MANAGER_DB_USER=admin
ENV KIWI_USER_MANAGER_DB_PASSWORD=12345

COPY ./app /app
COPY ./requirements.txt /app

RUN pip install -r requirements.txt 

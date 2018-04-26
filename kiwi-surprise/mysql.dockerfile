FROM mysql:5.7

COPY ./DatabaseImage/script.sql /docker-entrypoint-initdb.d

ENV MYSQL_ROOT_PASSWORD=12345

EXPOSE 3306

CMD ["mysqld"]

FROM mysql

COPY ./DatabaseImage/script.sql /docker-entrypoint-initdb.d

ENV MYSQL_ROOT_PASSWORD=12345

EXPOSE 3308

CMD ["mysqld"]
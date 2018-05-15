FROM mysql:5.7

COPY ./script.sql /docker-entrypoint-initdb.d

EXPOSE 3306

CMD ["mysqld"]

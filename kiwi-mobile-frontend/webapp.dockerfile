FROM httpd

COPY ./www /usr/local/apache2/htdocs

EXPOSE 80
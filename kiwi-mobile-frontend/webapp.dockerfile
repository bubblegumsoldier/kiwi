FROM httpd

COPY ./httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./www/ /usr/local/apache2/htdocs/

EXPOSE 80

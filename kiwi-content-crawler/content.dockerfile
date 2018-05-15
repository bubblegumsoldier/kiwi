FROM python:3

ENV PYTHONPATH=$PYTHONPATH:/kiwi
# One week in seconds
ENV RESET_PAGE_TIME=604800


COPY ./kiwi /kiwi
COPY ./requirements.txt /

WORKDIR /

EXPOSE 5000

RUN pip install -r requirements.txt 

ENTRYPOINT [ "python", "kiwi/main.py" ]

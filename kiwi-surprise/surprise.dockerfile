FROM python:3

ENV PYTHONPATH=$PYTHONPATH:/kiwi

ENV ALGO_PATH=algorithms/knn_user.py

COPY ./kiwi /kiwi
COPY ./requirements.txt /

WORKDIR /

RUN pip install numpy pandas
RUN pip install -r requirements.txt 

EXPOSE 8000
ENTRYPOINT [ "python", "kiwi/app.py" ]

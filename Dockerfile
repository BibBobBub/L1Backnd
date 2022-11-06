FROM python:3.9.2

ENV FLASK_APP=appfile

COPY requirements.txt /opt

RUN python3 -m pip install -r /opt/requirements.txt

COPY appfile /opt/appfile

WORKDIR /opt

CMD flask run --host 0.0.0.0 -p $PORT

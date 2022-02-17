FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY *.py .

COPY lib ./lib/

ENTRYPOINT [ "python3", "gb-util.py" ]

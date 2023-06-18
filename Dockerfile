FROM python:3.10.6-buster

RUN apt-get update && apt-get install -y libpq-dev python-dev gcc

WORKDIR /bot

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

CMD [ "python", "./src/main.py" ]
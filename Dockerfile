FROM python:3.8

WORKDIR /app

EXPOSE 5000

COPY ./app /app/app
COPY ./entrypoint.sh /app/entrypoint.sh
COPY ./requirements.txt /app/requirements.txt
# COPY ./migrations /app/migrations
# COPY ./database.py /app/database.py
COPY ./entry.py /app/entry.py

RUN chmod +x /app/entrypoint.sh

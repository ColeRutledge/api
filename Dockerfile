FROM python:3.8

WORKDIR /app

EXPOSE 5000

COPY ./app /app/app
COPY ./entrypoint.sh /app/entrypoint.sh
COPY ./requirements.txt /app/requirements.txt
COPY ./migrations /app/migrations
COPY ./db_seed.py /app/db_seed.py
COPY ./seed_market_sals.csv /app/seed_market_sals.csv
COPY ./seed_pos_metrics_mkt.csv /app/seed_pos_metrics_mkt.csv
COPY ./seed_positions.csv /app/seed_positions.csv
COPY ./entry.py /app/entry.py

RUN chmod +x /app/entrypoint.sh

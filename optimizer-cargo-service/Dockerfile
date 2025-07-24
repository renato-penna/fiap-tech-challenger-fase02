FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /app

RUN apt-get update && apt-get install -y gcc g++ libpq-dev python3-dev curl
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . .

RUN chmod -R 775 /app
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
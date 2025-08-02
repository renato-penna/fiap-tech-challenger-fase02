FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PYTHONPATH=/app
ENV PRODUCTS_API_URL=http://products-service:8000/products
ENV OPTIMIZER_API_URL=http://optimizer-service:8002/optimize/

EXPOSE 8501
ENTRYPOINT ["/entrypoint.sh"]

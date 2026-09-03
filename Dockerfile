FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p data/raw/bls data/processed data/curated

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

CMD ["python", "src/ingestion/bls_ingestion.py"]
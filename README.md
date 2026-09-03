## Running with Docker

Build the image:
docker build -t labor-market-intel .

Run the BLS ingestion pipeline:
docker run --env-file .env labor-market-intel

Run a different pipeline script:
docker run --env-file .env labor-market-intel python src/transformation/transform_oews_bulk.py
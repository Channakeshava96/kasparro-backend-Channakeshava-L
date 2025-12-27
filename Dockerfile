FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for psycopg2
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    sqlalchemy \
    psycopg2-binary \
    pydantic-settings \
    httpx

# Expose the port the API will run on
EXPOSE 8000

# Command to initialize the database, run the ETL, and then start the API server
CMD ["sh", "-c", "python -m core.init_db && python -m ingestion.etl_runner && uvicorn api.main:app --host 0.0.0.0 --port 8000"]

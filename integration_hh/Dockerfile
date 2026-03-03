FROM python:3.10

WORKDIR /integration_hh

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY integration_hh/ ./integration_hh/

EXPOSE 9090

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "9090"]
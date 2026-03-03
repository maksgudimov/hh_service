FROM python:3.10

WORKDIR /manager_crm_app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY manager_crm_app/ ./manager_crm_app/
COPY migrations/ ./migrations/
COPY alembic.ini .

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
FROM apache/airflow:3.1.5
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt && \
    pip install --force-reinstall --no-cache-dir browserforge && \
    python -c "from browserforge.headers import HeaderGenerator; HeaderGenerator()" || true

HEALTHCHECK CMD curl --fail http://localhost:8080/health || exit 1
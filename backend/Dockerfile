FROM python:3.11-slim

WORKDIR /app

COPY /backend /app/backend
COPY /model /app/model
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY pyproject.toml /app/pyproject.toml
COPY __init__.py /app/__init__.py


EXPOSE 8000

CMD ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8000"]

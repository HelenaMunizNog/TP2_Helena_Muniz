FROM python:3.9-slim-bullseye
LABEL authors="helenanogueira"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY regras_geradas.py .

COPY datasets /app/datasets/

CMD ["python", "regras_geradas.py"]
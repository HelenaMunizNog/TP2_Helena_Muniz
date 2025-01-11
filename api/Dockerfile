FROM python:3.9-slim-bullseye
LABEL authors="helenanogueira"

EXPOSE 9000

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY api.py .

ENV FLASK_APP=api.py
ENV MODEL_PATH=/app/data/rules.pkl

CMD ["python", "api.py"]
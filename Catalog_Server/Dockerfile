FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir Flask requests

EXPOSE 5000

CMD ["python", "main.py"]
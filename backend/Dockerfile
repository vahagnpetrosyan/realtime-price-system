FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./backend/

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["python", "backend/src/main.py"]
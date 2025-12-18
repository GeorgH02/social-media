FROM python:3.11-slim

WORKDIR /app

COPY backend/resize_service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend/resize_service/worker.py /app/worker.py
COPY backend/class_manager.py /app/class_manager.py

CMD ["python", "worker.py"]

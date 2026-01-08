FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    "numpy>=1.23.0,<2.0.0"

RUN pip install --no-cache-dir \
    torch==2.0.0+cpu \
    torchvision==0.15.0+cpu \
    --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir \
    transformers==4.36.0

COPY backend/ml_service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend/ml_service/download_model.py /app/download_model.py
COPY backend/ml_service/worker.py /app/worker.py
COPY backend/ml_service/ml.py /app/ml.py

RUN python /app/download_model.py

CMD ["python", "worker.py"]

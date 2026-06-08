FROM python:3.10-slim

# التعديل 1: إضافة g++ لضمان بناء حزم Whisper دون أخطاء
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# التعديل 2: فتح المنفذ 10000 وهو المنفذ الذي تتوقعه منصة Render
EXPOSE 10000

# التعديل 3: ربط Gunicorn بالمنفذ 10000 بدلاً من 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
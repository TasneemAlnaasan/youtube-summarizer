FROM python:3.10-slim

# تثبيت ffmpeg والأدوات الأساسية للنظام لمعالجة الصوت
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# نسخ وتثبيت المتطلبات من مجلد backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["gunicorn", "backend.app:app", "--bind", "0.0.0.0:10000"]
FROM python:3.10-slim

# 1. تثبيت حزم النظام والمترجمات (gcc, g++, ffmpeg)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. نسخ ملف المتطلبات وتجهيز بيئة البناء
COPY backend/requirements.txt .

# 3. تحديث الأدوات وتثبيت setuptools بالنسخة القياسية المستقرة
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 4. تثبيت المتطلبات مع تعطيل العزل لضمان رؤية 'pkg_resources' أثناء بناء Whisper
RUN pip install --no-cache-dir --no-build-isolation -r requirements.txt

# 5. نسخ باقي ملفات المشروع
COPY . .

EXPOSE 10000

CMD ["gunicorn", "backend.app:app", "--bind", "0.0.0.0:10000"]
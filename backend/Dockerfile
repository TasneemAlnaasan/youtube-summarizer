FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# التعديل هنا: نسخ ملف المتطلبات من مجلد backend المحلي
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip "setuptools<60.0.0" wheel
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي الملفات
COPY . .

EXPOSE 10000

# التعديل هنا: تشغيل التطبيق بالإشارة لمجلد backend إذا كان ملف app.py بداخله
# إذا كان ملف app.py في المجلد الرئيسي مباشرة اتركيها "app:app"
CMD ["gunicorn", "backend.app:app", "--bind", "0.0.0.0:10000"]
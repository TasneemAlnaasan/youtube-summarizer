FROM python:3.10-slim

# 1️⃣ أول خطوة: تثبيت كل حزم النظام المطلوبة لبناء مكتبات معالجة الصوت والفيديو
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    pkg-config \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libutil-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2️⃣ ثاني خطوة: تحديث أدوات بايثون الأساسية للـ Wheels
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 3️⃣ ثالث خطوة: نسخ وتثبيت الـ requirements بعد جاهزية النظام 100%
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ رابع خطوة: تحديث أداة التنزيل لتخطي حظر يوتيوب
RUN pip install --no-cache-dir --upgrade yt-dlp

COPY . .

EXPOSE 5000

CMD ["gunicorn", "app:app", "--chdir", "backend", "--bind", "0.0.0.0:5000"]
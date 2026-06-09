FROM python:3.10-slim

# 1️⃣ تنظيف وتحديث حزم النظام مع تخطي الأخطاء المؤقتة للمستودعات السحابية
RUN apt-get clean && \
    apt-get update --allow-releaseinfo-change-error --fix-missing && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    pkg-config \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2️⃣ تحديث أدوات بايثون الأساسية للـ Wheels
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 3️⃣ نسخ وتثبيت الـ requirements بعد جاهزية النظام
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ تحديث أداة التنزيل لتخطي حظر يوتيوب
RUN pip install --no-cache-dir --upgrade yt-dlp

COPY . .

EXPOSE 5000

CMD ["gunicorn", "app:app", "--chdir", "backend", "--bind", "0.0.0.0:5000"]
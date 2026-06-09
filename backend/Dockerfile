# 1️⃣ استخدام الصورة الكاملة المستقرة لمنع أخطاء التحديث
FROM python:3.10

# 2️⃣ تثبيت ffmpeg وحزم التطوير الخاصة بـ libav المطلوبة لبناء مكتبة av بنجاح
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libpostproc-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3️⃣ تحديث أدوات بايثون الأساسية للـ Wheels
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 4️⃣ نسخ وتثبيت المتطلبات (الآن ستُبنى مكتبة av بسلام)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ تحديث أداة التنزيل لتخطي حظر يوتيوب
RUN pip install --no-cache-dir --upgrade yt-dlp

COPY . .

EXPOSE 5000

CMD ["gunicorn", "app:app", "--chdir", "backend", "--bind", "0.0.0.0:5000"]
# 1️⃣ استخدام الصورة الكاملة المستقرة لضمان وجود أدوات المترجم
FROM python:3.10

# 2️⃣ تثبيت ffmpeg وكل حزم التطوير والربط الخاصة بـ libav و بايثون
RUN apt-get update && apt-get install -y \
    ffmpeg \
    pkg-config \
    python3-dev \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libpostproc-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3️⃣ تحديث أدوات بايثون لأحدث إصدار لضمان التعامل السليم مع الأكواد المصدرية
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 4️⃣ نسخ ملف المتطلبات وتثبيته مع خيار كسر العناد للمكتبات المترجمة
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --no-binary :all: av || pip install --no-cache-dir -r requirements.txt

# 5️⃣ تحديث أداة التنزيل لتخطي حظر يوتيوب
RUN pip install --no-cache-dir --upgrade yt-dlp

COPY . .

EXPOSE 5000

CMD ["gunicorn", "app:app", "--chdir", "backend", "--bind", "0.0.0.0:5000"]
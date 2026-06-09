# 🌟 التغيير الجوهري: الانتقال للنسخة الكاملة المجهزة بأدوات البناء تلقائياً
FROM python:3.10

# تثبيت ffmpeg فقط لمعالجة الصوت (هذه النسخة مستقرة جداً في التحديث)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# تحديث أدوات بايثون الأساسية
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# نسخ وتثبيت الـ requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# تحديث أداة التنزيل لتخطي حظر يوتيوب
RUN pip install --no-cache-dir --upgrade yt-dlp

COPY . .

EXPOSE 5000

CMD ["gunicorn", "app:app", "--chdir", "backend", "--bind", "0.0.0.0:5000"]
FROM python:3.11-slim

# Install system dependencies (including FFmpeg and basic build compilers)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
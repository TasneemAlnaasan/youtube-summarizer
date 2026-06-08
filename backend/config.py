import os
from dotenv import load_dotenv

# تحميل البيانات من .env
load_dotenv()

class Config:
    """الإعدادات الأساسية للتطبيق"""
    
    # مفتاح Google Gemini
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
    # إعدادات Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = True
    JSON_SORT_KEYS = False
    
    # CORS
    JSON_MIMETYPE = "application/json"
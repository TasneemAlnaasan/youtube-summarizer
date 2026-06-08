# 🎬 YouTube Summarizer

تطبيق ذكي يلخص فيديوهات YouTube باستخدام الذكاء الاصطناعي!

## ✨ الميزات

- استخراج نص الفيديو تلقائياً
- تلخيص ذكي بـ Google Gemini API
- واجهة سهلة وجميلة
- يعمل بدون تثبيت محلي

## 🛠️ المتطلبات

- Python 3.10+
- Flask
- Streamlit
- Google Generative AI API Key

## 📦 التثبيت

### محلياً:

```bash
# Clone Repository
git clone https://github.com/YOUR_USERNAME/youtube-summarizer.git
cd youtube-summarizer

# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
pip install -r requirements.txt
```

## 🚀 الاستخدام

### تشغيل محلي:

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
streamlit run app.py --server.address 0.0.0.0
```

### الاستخدام Online:
- Frontend: https://youtube-summarizer.streamlit.app
- Backend API: https://youtube-summarizer-api-so0i.onrender.com

## 📚 البنية
youtube-summarizer/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── runtime.txt
│   ├── Dockerfile
│   └── src/
│       └── youtube_handler.py
├── frontend/
│   ├── app.py
│   └── requirements.txt
├── .github/
│   └── workflows/
│       └── ci-cd.yml
└── README.md

## 🔑 متطلبات API

احصل على GOOGLE_API_KEY من:
https://ai.google.dev

أضفها في ملف `.env`:
GOOGLE_API_KEY=your_key_here
FLASK_ENV=production

## 🐳 Deployment

### Backend (Render + Docker):

اضغط "Connect Repository"
اختر youtube-summarizer
Build Command: (اتركها)
Start Command: (اتركها - Dockerfile بتتحكم)
أضف GOOGLE_API_KEY في Environment Variables


### Frontend (Streamlit Cloud):

اضغط "New app"
اختر github repo
Branch: main
File: frontend/app.py


## ✅ CI/CD

التطبيق بيستخدم GitHub Actions:
- Testing تلقائي عند كل push
- التحقق من المكتبات
- Deploy تلقائي على Render و Streamlit

شوف `.github/workflows/ci-cd.yml`

## 📊 Monitoring

تفعيل Uptime Robot:
https://uptimerobot.com
أضف: https://youtube-summarizer-api-so0i.onrender.com/health

## 🤝 المساهمة

Fork → Edit → Push → Pull Request

## 📝 الترخيص

MIT License

## 👨‍💻 المطور

تم بناؤه بـ ❤️ بـ Python و AI

---

## 🔗 الروابط المهمة

- [Google Generative AI Docs](https://ai.google.dev)
- [Flask Documentation](https://flask.palletsprojects.com)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Render Docs](https://render.com/docs)

## ⚡ المشاكل المعروفة

- YouTube IP Blocking: استخدم Mock Data
- Python 3.14 Incompatibility: استخدم Python 3.10

---

**آخر تحديث:** 2026-05-27
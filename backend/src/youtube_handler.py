

import google.generativeai as genai
from config import Config
import re
from youtube_transcript_api import YouTubeTranscriptApi


def validate_youtube_url(url: str) -> bool:
    """
    التحقق من أن الرابط رابط YouTube صحيح
    
    Args:
        url (str): رابط YouTube
        
    Returns:
        bool: True لو صحيح، False لو خطأ
    """
    
    # التحقق من أن الرابط يحتوي youtube.com أو youtu.be
    # والرابط يبدأ بـ https://
    if ("youtube.com" in url or "youtu.be" in url) and url.startswith("https://"):
        return True
    else:
        return False


def extract_youtube_id(url: str) -> str:
    """
    استخراج YouTube Video ID من الرابط
    
    Args:
        url (str): رابط YouTube
        
    Returns:
        str: YouTube Video ID
        
    مثال:
        https://www.youtube.com/watch?v=abc123 → abc123
        https://youtu.be/abc123 → abc123
    """
    
    # Regex pattern لاستخراج ID
    # [a-zA-Z0-9_-]+ = حروف وأرقام و underscore و dash
    pattern = r'(?:youtube\.com\/watch\?v=|youtu\.be\/|v\/|embed\/)([a-zA-Z0-9_-]+)'
    
    # ابحث عن النمط في الرابط
    match = re.search(pattern, url)
    
    if match:
        # أرجع الـ ID (المجموعة الأولى من الـ match)
        return match.group(1)
    
    # لو ما لاقيت ID
    return None

def get_youtube_transcript(video_id: str, use_mock: bool = False) -> str:
    """
    استخراج نص الفيديو (Transcript) من YouTube
    
    Args:
        video_id (str): معرف الفيديو
        use_mock (bool): استخدم Mock Data للاختبار؟
        
    Returns:
        str: النص الكامل للفيديو أو Mock Data
    """
    
    # الخيار الأول: Mock Data (للاختبار المحلي)
    if use_mock:
        mock_transcript = """
        Welcome to our YouTube Summarizer application.
        This is a test video about artificial intelligence and machine learning.
        We are building a powerful tool that extracts transcripts from YouTube videos.
        The application uses Google Gemini API for summarization.
        This project demonstrates how to build production-ready applications with Python.
        We use Flask for the backend and Streamlit for the frontend.
        The entire application is deployed on free cloud services.
        This is perfect for learning AI engineering and building AI-powered applications.
        """
        return mock_transcript
    
    # الخيار الثاني: Real Data (من YouTube)
    try:
        # أنشئ instance من المكتبة
        api = YouTubeTranscriptApi()
        
        # احصل على قائمة الترجمات
        transcript_list = api.list(video_id)
        
        # ابحث عن الترجمة بالإنجليزي
        transcript = transcript_list.find_transcript(['en'])
        
        # احصل على النص
        captions = transcript.fetch()
        
        # اجمع النصوص
        texts = [item['text'] for item in captions]
        full_text = ' '.join(texts)
        
        return full_text
        
    except Exception as e:
        return f"Error extracting transcript: {str(e)}"


def summarize_transcript(transcript: str, use_mock: bool = False) -> str:
    """
    تلخيص النص باستخدام Google Gemini
    
    Args:
        transcript (str): النص المراد تلخيصه
        use_mock (bool): استخدم Mock Summary للاختبار؟
        
    Returns:
        str: الملخص
    """
    
    # الخيار الأول: Mock Summary (للاختبار المحلي)
    if use_mock:
        mock_summary = """
        This video provides a comprehensive overview of AI engineering fundamentals.
        It covers key concepts including prompt engineering, RAG (Retrieval-Augmented Generation), 
        and vector databases. The content demonstrates how to build production-ready AI applications 
        using Python, Flask, and Streamlit. The tutorial emphasizes best practices for API integration, 
        error handling, and deployment strategies. Overall, it's an excellent resource for learning 
        modern AI engineering techniques and practical implementation skills.
        """
        return mock_summary
    
    # الخيار الثاني: Real Summary (من Google Gemini)
    try:
        # أعدّ مفتاح API
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        
        # أنشئ نموذج Gemini
        model = genai.GenerativeModel('gemini-pro')
        
        # اكتب الـ Prompt
        prompt = f"""
        Please summarize the following video transcript in 3-5 clear and concise sentences.
        Focus on the main points and key takeaways.
        
        Transcript:
        {transcript}
        
        Summary:
        """
        
        # اطلب التلخيص
        response = model.generate_content(prompt)
        
        # أرجع الملخص
        return response.text
        
    except Exception as e:
        return f"Error summarizing transcript: {str(e)}"
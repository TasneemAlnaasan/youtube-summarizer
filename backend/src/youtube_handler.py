import google.generativeai as genai
from config import Config
import re
from youtube_transcript_api import YouTubeTranscriptApi

def validate_youtube_url(url: str) -> bool:
    if ("youtube.com" in url or "youtu.be" in url) and url.startswith("https://"):
        return True
    return False

def extract_youtube_id(url: str) -> str:
    pattern = r'(?:youtube\.com\/watch\?v=|youtu\.be\/|v\/|embed\/)([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_youtube_transcript(video_id: str, use_mock: bool = False) -> str:
    """استخراج نص الفيديو بدعم كامل لجميع اللغات (العربية والإنجليزية والترجمة التلقائية)"""
    if use_mock:
        return "Welcome to our YouTube Summarizer application test transcript."
    
    try:
        # الحل الذكي: جلب الترجمة مباشرة ودعم العربية والانجليزية وأي لغات أخرى
        captions = YouTubeTranscriptApi.get_transcript(video_id, languages=['ar', 'en', 'en-US'])
        
        # تجميع النصوص
        texts = [item['text'] for item in captions]
        full_text = ' '.join(texts)
        return full_text
        
    except Exception as e:
        # محاولة أخيرة: إذا لم يجد عربي أو إنجليزي، يسحب أي لغة متوفرة في الفيديو رغماً عنه
        try:
            print("🔄 محاولة سحب أي لغة متوفرة أخرى...")
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            # سحب أول ترجمة متاحة للفيديو أياً كانت لغتها
            captions = transcript_list.get_variable_transcript().fetch()
            texts = [item['text'] for item in captions]
            return ' '.join(texts)
        except Exception as fallback_error:
            return f"Error extracting transcript: لم نتمكن من سحب الترجمة. قد يكون يوتيوب قد حظر السيرفر مؤقتاً. التفاصيل: {str(fallback_error)}"


def summarize_transcript(transcript: str, use_mock: bool = False) -> str:
    if use_mock:
        return "This is a mock summary for testing purposes."
        
    if transcript.startswith("Error extracting transcript"):
        return "لا يمكن توليد ملخص لأن عملية استخراج النص فشلت."
        
    try:
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        
        # التحديث المصيري لضمان العمل المجاني والمستقر
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Please summarize the following video transcript in 3-5 clear and concise sentences.
        Focus on the main points and key takeaways.
        
        Transcript:
        {transcript}
        
        Summary:
        """
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Error summarizing transcript: {str(e)}"
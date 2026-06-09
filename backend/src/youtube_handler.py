import re
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from config import Config

def validate_youtube_url(url: str) -> bool:
    """التحقق من صحة رابط اليوتيوب"""
    if url and ("youtube.com" in url or "youtu.be" in url) and url.startswith("https://"):
        return True
    return False

def extract_youtube_id(url: str) -> str:
    """استخراج الـ Video ID"""
    pattern = r'(?:youtube\.com\/watch\?v=|youtu\.be\/|v\/|embed\/)([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_youtube_transcript(video_id: str, use_mock: bool = False) -> str:
    """
    استخراج النص من YouTube Captions
    استخدم الطريقة الصحيحة بدون api = YouTubeTranscriptApi()
    """
    
    if use_mock:
        return "Welcome to our YouTube Summarizer application. This is a test video."
    
    print(f"📝 جاري استخراج Captions للفيديو: {video_id}")
    
    try:
        # الطريقة الصحيحة - مباشر!
        captions = YouTubeTranscriptApi.get_transcript(
            video_id, 
            languages=['ar', 'en']
        )
        
        texts = [item['text'] for item in captions]
        result = ' '.join(texts)
        
        if not result.strip():
            return "Error: الفيديو لا يحتوي على ترجمة"
        
        print(f"✅ تم استخراج {len(texts)} عنصر!")
        return result
    
    except Exception as e:
        error_msg = str(e)
        print(f"❌ خطأ: {error_msg}")
        return f"Error extracting transcript: هذا الفيديو ليس عنده captions. استخدم فيديو فيه ترجمة."

def summarize_transcript(transcript: str, use_mock: bool = False) -> str:
    """تلخيص النص بـ gemini-1.5-flash (الصحيح!)"""
    
    if use_mock:
        return "This is a test summary of the video content."
    
    # تحقق من خطأ
    if transcript.startswith("Error"):
        return transcript
    
    try:
        print("🤖 جاري التلخيص...")
        
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        
        # استخدم gemini-1.5-flash (الصحيح!)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Please summarize the following video transcript in 3-5 clear and concise sentences.
        Focus on the main points and key takeaways.
        
        Transcript:
        {transcript}
        
        Summary:
        """
        
        response = model.generate_content(prompt)
        summary = response.text
        
        print("✅ تم التلخيص بنجاح!")
        return summary
    
    except Exception as e:
        error_msg = str(e)
        print(f"❌ خطأ في التلخيص: {error_msg}")
        return f"Error summarizing transcript: {error_msg}"
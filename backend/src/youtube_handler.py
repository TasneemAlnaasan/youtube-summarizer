import google.generativeai as genai
from config import Config
import re
from youtube_transcript_api import YouTubeTranscriptApi

def validate_youtube_url(url: str) -> bool:
    """التحقق من صحة رابط اليوتيوب المرسل"""
    if url and ("youtube.com" in url or "youtu.be" in url) and url.startswith("https://"):
        return True
    return False

def extract_youtube_id(url: str) -> str:
    """استخراج الـ Video ID من الرابط"""
    pattern = r'(?:youtube\.com\/watch\?v=|youtu\.be\/|v\/|embed\/)([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_youtube_transcript(video_id: str, use_mock: bool = False) -> str:
    """جلب الترجمة الحقيقية للفيديو مباشرة بدعم العربية والإنجليزية والتلقائية"""
    if use_mock:
        return "Welcome to our YouTube Summarizer application test transcript."
    
    print(f"📝 جاري جلب الترجمة للفيديو: {video_id}")
    try:
        # المحاولة الأولى: جلب الترجمة باللغات الأساسية المتوقعة (العربية أو الإنجليزية)
        captions = YouTubeTranscriptApi.get_transcript(video_id, languages=['ar', 'en', 'en-US'])
        texts = [item['text'] for item in captions]
        return ' '.join(texts)
        
    except Exception as e:
        try:
            # المحاولة الثانية (الحل الذكي): إذا لم يجد اللغات السابقة، يسحب أول ترجمة متوفرة في الفيديو رغماً عنه (حتى لو تلقائية)
            print("🔄 لم يجد العربية أو الإنجليزية مباشرة، جاري البحث عن أي ترجمة متاحة...")
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            captions = transcript_list.get_variable_transcript().fetch()
            texts = [item['text'] for item in captions]
            return ' '.join(texts)
        except Exception as fallback_error:
            return f"Error extracting transcript: لم نتمكن من سحب الترجمة. تأكدي أن الفيديو يحتوي على كابشن أو ترجمة مصاحبة فعلاً. التفاصيل: {str(fallback_error)}"

def summarize_transcript(transcript: str, use_mock: bool = False) -> str:
    """تلخيص النص الحقيقي المستخرج بواسطة نموذج gemini-1.5-flash المجاني والسريع"""
    if use_mock:
        return "This is a mock summary for testing purposes."
        
    if transcript.startswith("Error extracting transcript"):
        return "لا يمكن توليد ملخص لأن عملية استخراج النص من الفيديو فشلت."
        
    try:
        genai.configure(api_key=Config.GOOGLE_API_KEY)
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
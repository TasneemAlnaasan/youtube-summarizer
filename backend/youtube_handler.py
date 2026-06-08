import re
import os
import subprocess
from faster_whisper import WhisperModel  
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from config import Config

# تحميل Faster-Whisper model مرة واحدة بشكل ذكي وخفيف
try:
    whisper_model = WhisperModel("tiny", device="cpu", compute_type="int8")
    print("🤖 Faster-Whisper (Tiny) loaded successfully on CPU!")
except Exception as e:
    print(f"⚠️ Failed to load Faster-Whisper: {str(e)}")
    whisper_model = None

def validate_youtube_url(url: str) -> bool:
    if url and ("youtube.com" in url or "youtu.be" in url) and url.startswith("https://"):
        return True
    return False

def extract_youtube_id(url: str) -> str:
    pattern = r'(?:youtube\.com\/watch\?v=|youtu\.be\/|v\/|embed\/)([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_youtube_transcript(video_id: str, use_mock: bool = False) -> str:
    """
    استخرج النص من الفيديو:
    1️⃣ محاولة أولى: YouTube Captions (سريع + مجاني)
    2️⃣ محاولة ثانية: Faster-Whisper (عند عدم وجود الكابشن الجاهز)
    """
    if use_mock:
        return "Welcome to our YouTube Summarizer application test transcript."
    
    print("📝 جاري محاولة استخراج Captions الجاهزة...")
    try:
        # التعديل الأول الصريح: جلب الكابشن مباشرة دون أي دالة 'list' قديمة
        captions = YouTubeTranscriptApi.get_transcript(video_id, languages=['ar', 'en'])
        texts = [item['text'] for item in captions]
        result = ' '.join(texts)
        print("✅ Captions extracted successfully!")
        return result
    
    except Exception as e:
        print(f"❌ Captions not found or failed: {str(e)}")
        print("🎤 Switching to Faster-Whisper Speech-to-Text...")
        
        try:
            return transcribe_with_whisper(video_id)
        except Exception as whisper_error:
            print(f"❌ Faster-Whisper also failed: {str(whisper_error)}")
            # نرفع الخطأ لكي يراه الباك إند ويتعامل معه بشكل صحيح
            raise Exception(f"Could not extract transcript via Captions or Whisper. Details: {str(whisper_error)}")

def transcribe_with_whisper(video_id: str) -> str:
    """استخدم Faster-Whisper لاستخراج النص من الصوت"""
    if whisper_model is None:
        raise Exception("Faster-Whisper model is not available/loaded")
    
    print("📥 جاري تحميل الصوت من YouTube عبر yt-dlp...")
    audio_file = download_youtube_audio(video_id)
    
    try:
        print("🎤 جاري تحويل الصوت لنص بواسطة Faster-Whisper...")
        segments, info = whisper_model.transcribe(audio_file, beam_size=5)
        transcript = "".join([segment.text for segment in segments])
        
        # التأكد من أن النص ليس فارغاً
        if not transcript.strip():
            raise Exception("Whisper generated an empty transcript.")
            
        print(f"✅ Transcription complete! Detected language: {info.language}")
        return transcript
        
    finally:
        if os.path.exists(audio_file):
            os.remove(audio_file)
            print("🗑️ Cleaned up temporary files")

def download_youtube_audio(video_id: str) -> str:
    """نزل الصوت من YouTube"""
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    output_file = f"/tmp/{video_id}.mp3"
    
    cmd = [
        "yt-dlp",
        "-x",  
        "--audio-format", "mp3",
        "-o", output_file,
        youtube_url
    ]
    
    try:
        print(f"⏳ Downloading audio file...")
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ Audio downloaded and saved at {output_file}")
        return output_file
    except Exception as e:
        raise Exception(f"Failed to download audio via yt-dlp: {str(e)}")

def summarize_transcript(transcript: str, use_mock: bool = False) -> str:
    if use_mock:
        return "This is a mock summary for testing purposes."
    try:
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        
        # التعديل الثاني الجوهري: تحديث النموذج إلى gemini-1.5-flash المدعوم حالياً ومجاناً
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
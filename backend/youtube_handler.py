import re
import os
import subprocess
import whisper
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from ..config import Config

# تحميل Whisper model مرة واحدة
try:
    whisper_model = whisper.load_model("base")
except:
    whisper_model = None

def validate_youtube_url(url: str) -> bool:
    if ("youtube.com" in url or "youtu.be" in url) and url.startswith("https://"):
        return True
    else:
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
    2️⃣ محاولة ثانية: Whisper (بطيء لكن يشتغل دائماً)
    """
    
    if use_mock:
        return """
        Welcome to our YouTube Summarizer application.
        This is a test video about artificial intelligence and machine learning.
        We are building a powerful tool that extracts transcripts from YouTube videos.
        The application uses Google Gemini API for summarization.
        """
    
    # محاولة 1: YouTube Captions
    print("📝 جاري محاولة استخراج Captions...")
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        transcript = transcript_list.find_transcript(['ar', 'en'])
        captions = transcript.fetch()
        texts = [item['text'] for item in captions]
        result = ' '.join(texts)
        print("✅ Captions extracted successfully!")
        return result
    
    except Exception as e:
        print(f"❌ Captions not found: {str(e)}")
        print("🎤 Switching to Whisper Speech-to-Text...")
        
        # محاولة 2: Whisper
        try:
            return transcribe_with_whisper(video_id)
        except Exception as whisper_error:
            print(f"❌ Whisper also failed: {str(whisper_error)}")
            return f"Error: Could not extract transcript - {str(whisper_error)}"

def transcribe_with_whisper(video_id: str) -> str:
    """استخدم Whisper لاستخراج النص من الصوت"""
    
    if whisper_model is None:
        raise Exception("Whisper model not loaded")
    
    print("📥 جاري تحميل الصوت من YouTube...")
    
    # نزل الصوت
    audio_file = download_youtube_audio(video_id)
    
    try:
        print("🎤 جاري تحويل الصوت لنص...")
        result = whisper_model.transcribe(audio_file, language="ar")
        transcript = result['text']
        print("✅ Transcription complete!")
        return transcript
    
    finally:
        # احذف الملف المؤقت
        if os.path.exists(audio_file):
            os.remove(audio_file)
            print("🗑️ Cleaned up temporary files")

def download_youtube_audio(video_id: str) -> str:
    """نزل الصوت من YouTube"""
    
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    output_file = f"/tmp/{video_id}.mp3"
    
    cmd = [
        "yt-dlp",
        "-x", # استخرج الصوت فقط
        "--audio-format", "mp3",
        "-o", output_file,
        youtube_url
    ]
    
    try:
        print(f"⏳ Downloading audio...")
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ Audio downloaded")
        return output_file
    except Exception as e:
        raise Exception(f"Failed to download audio: {str(e)}")

def summarize_transcript(transcript: str, use_mock: bool = False) -> str:
    if use_mock:
        return """
        This video provides a comprehensive overview of AI engineering fundamentals.
        It covers key concepts including prompt engineering, RAG systems,
        and vector databases. The tutorial emphasizes best practices for API integration,
        error handling, and deployment strategies.
        """
    try:
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
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
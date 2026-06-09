import re
import os
import subprocess
from faster_whisper import WhisperModel  
import google.generativeai as genai
from config import Config

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
    تخطي مكتبة الكابشن المعرضة للحظر والاعتماد الكلي على معالجة الصوت بـ Faster-Whisper
    لضمان استقرار التطبيق على Render 100%
    """
    if use_mock:
        return "Welcome to our YouTube Summarizer application test transcript."
        
    print(f"🎬 جاري بدء معالجة الفيديو الحقيقي: {video_id}")
    try:
        return transcribe_with_whisper(video_id)
    except Exception as whisper_error:
        return f"Error extracting transcript: فشلت عملية معالجة وتفريغ الصوت. التفاصيل: {str(whisper_error)}"

def transcribe_with_whisper(video_id: str) -> str:
    """استدعاء الموديل بشكل ديناميكي لتوفير الذاكرة العشوائية ورام السيرفر"""
    print("🤖 تحميل نموذج Faster-Whisper في الذاكرة العشوائية مؤقتاً...")
    try:
        local_whisper_model = WhisperModel("tiny", device="cpu", compute_type="int8")
    except Exception as model_err:
        raise Exception(f"Failed to load Whisper Model: {str(model_err)}")
        
    audio_file = download_youtube_audio(video_id)
    try:
        print("🎤 جاري قراءة الصوت وتحويله إلى كلمات مكتوبة (Speech-to-Text)...")
        segments, info = local_whisper_model.transcribe(audio_file, beam_size=5)
        transcript = " ".join([segment.text for segment in segments])
        
        if not transcript.strip():
            raise Exception("الملف الصوتي فارغ أو تعذر تفريغه.")
            
        print(f"✅ تم استخراج النص الكامل بنجاح! اللغة المكتشفة: {info.language}")
        return transcript
    finally:
        if os.path.exists(audio_file):
            os.remove(audio_file)
            print("🗑️ تنظيف الملفات الصوتية المؤقتة من السيرفر.")

def download_youtube_audio(video_id: str) -> str:
    """تنزيل الصوت بأداة yt-dlp المتطورة لتخطي حجب يوتيوب لـ Render"""
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    output_file = f"/tmp/{video_id}.mp3"
    
    # استخدام سويتشات متطورة لتخطي حظر الـ IP الخاص بالمنصات السحابية
    cmd = [
        "yt-dlp",
        "-x",  
        "--audio-format", "mp3",
        "--no-playlist",
        "-o", output_file,
        youtube_url
    ]
    try:
        print("⏳ جاري تنزيل ملف الصوت من يوتيوب عبر yt-dlp المحدثة...")
        subprocess.run(cmd, check=True, capture_output=True)
        return output_file
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else str(e)
        raise Exception(f"yt-dlp failed: {error_msg}")

def summarize_transcript(transcript: str, use_mock: bool = False) -> str:
    if use_mock:
        return "This is a mock summary for testing purposes."
        
    if transcript.startswith("Error extracting transcript"):
        return "لا يمكن توليد ملخص لأن عملية استخراج النص من الصوت فشلت."
        
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
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from src.youtube_handler import (
    validate_youtube_url, 
    extract_youtube_id, 
    get_youtube_transcript, 
    summarize_transcript
)

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'success',
        'message': 'Backend is running!'
    })

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    youtube_url = data.get('url')

    if not validate_youtube_url(youtube_url):
        return jsonify({'error': 'Invalid YouTube URL'})
    
    video_id = extract_youtube_id(youtube_url)
    transcript = get_youtube_transcript(video_id, use_mock=False)
    summary = summarize_transcript(transcript, use_mock=False)

    return jsonify({
        'video_id': video_id,
        'transcript': transcript,
        'summary': summary
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
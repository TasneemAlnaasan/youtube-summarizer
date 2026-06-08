import os
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
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    youtube_url = data.get('url')

    if not validate_youtube_url(youtube_url):
        return jsonify({'error': 'Invalid YouTube URL'}), 400
    
    video_id = extract_youtube_id(youtube_url)
    
    try:
        transcript = get_youtube_transcript(video_id, use_mock=False)
        summary = summarize_transcript(transcript, use_mock=False)

        return jsonify({
            'video_id': video_id,
            'transcript': transcript,
            'summary': summary
        })
    except Exception as e:
        return jsonify({
            'error': 'Failed to process video',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
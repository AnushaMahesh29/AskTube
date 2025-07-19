import os
import re 
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

DATA_DIR = "data/transcripts"

def extract_video_id(url):
   
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    raise ValueError("Invalid YouTube URL")

def load_transcript_from_file(video_id):
    
    file_path = os.path.join(DATA_DIR, f"{video_id}.txt")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    raise FileNotFoundError(f"Transcript file for video ID {video_id} not found.")

def save_transcript_to_file(video_id, transcript):
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, f"{video_id}.txt")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(transcript)

def get_transcript(video_id: str) -> str:
    try:
        cached = load_transcript_from_file(video_id)
        if cached:
            return cached
    except FileNotFoundError:
        pass  # Proceed to fetch from YouTube

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([seg["text"] for seg in transcript])
        save_transcript_to_file(video_id, transcript_text)
        return transcript_text
    except (TranscriptsDisabled, NoTranscriptFound):
        raise ValueError(f"Transcript not available for video ID {video_id}.")

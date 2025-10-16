import os
import json
import uuid
import datetime
import subprocess
import logging
from gtts import gTTS
import requests

from config import INPUT_FILE, OUTPUT_DIR, AVATAR_IMAGE, WAV2LIP_DIR, WAV2LIP_CHECKPOINT, GEMINI_API_KEY, GEMINI_API_URL

logging.basicConfig(filename='logs/avatar.log', level=logging.INFO)

def read_input():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('user_text', '').strip()

def get_llm_response(prompt):
    headers = {'Content-Type': 'application/json'}
    params = {'key': GEMINI_API_KEY}
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload)
    response.raise_for_status()
    result = response.json()
    return result['candidates'][0]['content']['parts'][0]['text']

def text_to_speech(text, audio_path):
    tts = gTTS(text=text, lang='en') 
    tts.save(audio_path)

def generate_video(audio_path, video_path):
    command = [
        'python', os.path.join(WAV2LIP_DIR, 'inference.py'),
        '--checkpoint_path', WAV2LIP_CHECKPOINT,
        '--face', AVATAR_IMAGE,
        '--audio', audio_path,
        '--outfile', video_path
    ]
    subprocess.run(command, check=True)

def main():
    user_text = read_input()
    response_text = get_llm_response(user_text)
    unique_id = uuid.uuid4().hex
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    audio_path = os.path.join(OUTPUT_DIR, f"response_{timestamp}_{unique_id}.mp3")
    text_to_speech(response_text, audio_path)

    video_path = os.path.join(OUTPUT_DIR, f"video_{timestamp}_{unique_id}.mp4")
    generate_video(audio_path, video_path)

    print(json.dumps({"video_path": video_path}))

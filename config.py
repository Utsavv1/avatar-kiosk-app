import os

INPUT_FILE = 'input.json'
OUTPUT_DIR = 'output'
AVATAR_IMAGE = 'avatar1.jpg'
WAV2LIP_DIR = 'wav2lip'
WAV2LIP_CHECKPOINT = os.path.join(WAV2LIP_DIR, 'checkpoints', 'wav2lip_gan.pth')
GEMINI_API_KEY = 'AIzaSyAy00DV8ewg2EAQYjKzMetfHzGE0zky7qg'
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent'

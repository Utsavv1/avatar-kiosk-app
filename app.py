import os
import cv2
import time
import subprocess
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai

AVATAR_IMAGE = "avatar.jpg"
WAV2LIP_CHECKPOINT = "wav2lip.pth"
WAV2LIP_SCRIPT = "D:/utsav1/voice-assistant/Wav2Lip/inference.py"
TEMP_AUDIO = "temp/input.wav"
TEMP_VIDEO = "temp/result.mp4"

genai.configure(api_key="AIzaSyBx4i3Z684q0pZKzhQs2heXy2FBpykVpMU")
model = genai.GenerativeModel("gemini-1.5-flash")
recognizer = sr.Recognizer()

def generate_speech(text, path=TEMP_AUDIO):
    tts = gTTS(text)
    tts.save(path)
    print("✅ Voice saved.")

def listen():
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        try:
            query = recognizer.recognize_google(audio)
            print("👤 You:", query)
            return query
        except Exception as e:
            print("⚠️ Mic Error:", e)
            return ""

def ask_gemini(query):
    try:
        response = model.generate_content(query)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini Error:", e)
        return "I'm sorry, I couldn't understand."

def run_wav2lip():
    print("🛠️ Generating video with lip sync...")
    cmd = [
        "python", WAV2LIP_SCRIPT,
        "--checkpoint_path", WAV2LIP_CHECKPOINT,
        "--face", AVATAR_IMAGE,
        "--audio", TEMP_AUDIO,
        "--outfile", TEMP_VIDEO
    ]
    subprocess.run(cmd)

def play_video(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print("❌ Error: Could not open video.")
        return

    print("🎬 Showing avatar video...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("🧑‍💻 AI Avatar Speaking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    os.makedirs("temp", exist_ok=True)
    print("🚀 AI Avatar Assistant Started. Press Ctrl+C to stop.")

    while True:
        query = listen()
        if query:
            answer = ask_gemini(query)
            print("🤖 Gemini:", answer)
            generate_speech(answer)
            run_wav2lip()
            play_video(TEMP_VIDEO)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Exiting.")

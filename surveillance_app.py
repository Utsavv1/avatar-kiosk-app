import cv2
import datetime
import logging
from deepface import DeepFace

# Setup logging
logging.basicConfig(filename='logs/surveillance.log', level=logging.INFO)

# Suspicious emotions to trigger alerts
SUSPICIOUS_EMOTIONS = ['angry', 'fear', 'disgust']

# Race-to-country mapping
RACE_COUNTRY_MAP = {
    'white': 'Europe / North America',
    'black': 'Africa / Diaspora',
    'asian': 'East/Southeast Asia',
    'indian': 'South Asia',
    'middle eastern': 'Middle East / N. Africa',
    'latino hispanic': 'Latin America / Spain'
}

def analyze_and_display(frame):
    suspicious_detected = False

    try:
        results = DeepFace.analyze(
            frame,
            actions=['age', 'gender', 'emotion', 'race'],
            enforce_detection=False,
        )

        if isinstance(results, dict):
            results = [results]

        for person in results:
            age = person.get('age')
            gender = person.get('gender')
            emotion = person.get('dominant_emotion')
            race = person.get('dominant_race', '').lower()
            region = person.get('region', {})

            country_guess = RACE_COUNTRY_MAP.get(race, 'Unknown Region')

            x, y, w, h = region.get('x', 0), region.get('y', 0), region.get('w', 0), region.get('h', 0)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            info_lines = [
                f"Gender: {gender}",
                f"Age: {age}",
                f"Emotion: {emotion}",
                f"Ethnicity: {race.title()}",
                f"Guess: {country_guess}"
            ]

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            thickness = 1
            line_height = 18

            for i, text in enumerate(info_lines[::-1]):  # Draw from bottom to top
                text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
                text_x = x
                text_y = max(y - 5 - i * line_height, 10)
                cv2.rectangle(
                    frame,
                    (text_x, text_y - text_size[1] - 4),
                    (text_x + text_size[0] + 4, text_y + 2),
                    (0, 255, 0),
                    -1
                )
                cv2.putText(frame, text, (text_x + 2, text_y), font, font_scale, (0, 0, 0), thickness)

            if emotion.lower() in SUSPICIOUS_EMOTIONS:
                suspicious_detected = True
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                alert_file = f"output/alert_{timestamp}.txt"
                with open(alert_file, "w") as f:
                    f.write(f"⚠️ Suspicious emotion '{emotion}' detected at {timestamp}\n")
                logging.warning(f"⚠️ Suspicious emotion detected: {emotion}")

    except Exception as e:
        logging.error(f"Error analyzing frame: {e}")

    return suspicious_detected

def run_surveillance():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        logging.error("❌ Failed to open webcam.")
        print("Error: Cannot access camera.")
        return

    print("📹 Surveillance started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            logging.warning("⚠️ Failed to read frame from camera.")
            break

        suspicious = analyze_and_display(frame)

        if suspicious:
            cv2.putText(
                frame, "⚠️ Suspicious Activity Detected!",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2
            )

        cv2.imshow("Live Surveillance Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_surveillance()

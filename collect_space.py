import os
import pickle
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode

dataset_size = 100
SPACE_LABEL = 26

MODEL_PATH = './hand_landmarker.task'

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.3,
    min_hand_presence_confidence=0.3
)

hand_landmarker = HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

if os.path.exists('data.pickle'):
    with open('data.pickle', 'rb') as f:
        existing = pickle.load(f)
    data = existing['data']
    labels = existing['labels']
    print(f"Loaded existing data: {len(data)} samples")
else:
    data = []
    labels = []
    print("No existing data found, starting fresh.")

print('Get ready to show SPACE gesture  |  Press Q to start collecting')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    results = hand_landmarker.detect(mp_image)

    if results.hand_landmarks:
        landmarks = results.hand_landmarks[0]
        for lm in landmarks:
            cx, cy = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
            cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)
        status_color = (0, 255, 0)
        status_text = "Hand Detected! Press Q to collect"
    else:
        status_color = (0, 0, 255)
        status_text = "NO Hand Detected - Show your hand!"

    cv2.rectangle(frame, (0, 0), (frame.shape[1], 70), (0, 0, 0), -1)
    cv2.putText(frame, 'Gesture: SPACE', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(frame, status_text, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, status_color, 2)

    cv2.imshow('Collect Space Data', frame)
    if cv2.waitKey(25) == ord('q'):
        break

counter = 0
while counter < dataset_size:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    results = hand_landmarker.detect(mp_image)

    if results.hand_landmarks:
        landmarks = results.hand_landmarks[0]
        x_ = [lm.x for lm in landmarks]
        y_ = [lm.y for lm in landmarks]
        data_aux = []

        for lm in landmarks:
            cx, cy = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
            cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

        for lm in landmarks:
            data_aux.append(lm.x - min(x_))
            data_aux.append(lm.y - min(y_))

        data.append(data_aux)
        labels.append(SPACE_LABEL)
        counter += 1
        detect_color = (0, 255, 0)
        detect_text = f"Collecting... {counter}/{dataset_size}"
    else:
        detect_color = (0, 0, 255)
        detect_text = "NO Hand! Move hand into frame"

    cv2.rectangle(frame, (0, 0), (frame.shape[1], 70), (0, 0, 0), -1)
    cv2.putText(frame, 'Gesture: SPACE', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(frame, detect_text, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, detect_color, 2)

    cv2.imshow('Collect Space Data', frame)
    cv2.waitKey(25)

print(f'Done collecting SPACE gesture ({counter} samples)')

cap.release()
cv2.destroyAllWindows()
hand_landmarker.close()

with open('data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

print(f"Data saved to data.pickle (total: {len(data)} samples)")
print("Now run train_classifier.py to retrain the model!")

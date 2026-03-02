import pickle
import cv2
import time
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode

model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

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

labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H',
               8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P',
               16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W',
               23: 'X', 24: 'Y', 25: 'Z', 26: 'SPACE'}

sentence = ""
current_char = ""
char_count = 0
STABLE_THRESHOLD = 15

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    results = hand_landmarker.detect(mp_image)

    predicted_character = ""

    if results.hand_landmarks:
        landmarks = results.hand_landmarks[0]
        x_ = [lm.x for lm in landmarks]
        y_ = [lm.y for lm in landmarks]
        data_aux = []

        for lm in landmarks:
            cx, cy = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        for lm in landmarks:
            data_aux.append(lm.x - min(x_))
            data_aux.append(lm.y - min(y_))

        if len(data_aux) == 42:
            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = labels_dict[int(prediction[0])]

            if predicted_character == current_char:
                char_count += 1
            else:
                current_char = predicted_character
                char_count = 1

            if char_count == STABLE_THRESHOLD:
                if current_char == 'SPACE':
                    sentence += " "
                else:
                    sentence += current_char

    else:
        current_char = ""
        char_count = 0

    cv2.rectangle(frame, (0, 0), (frame.shape[1], 90), (0, 0, 0), -1)

    if predicted_character:
        cv2.putText(frame, predicted_character, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, "No hand", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    display_text = sentence[-40:] if len(sentence) > 40 else sentence
    cv2.putText(frame, f"Text: {display_text}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(frame, "Q:Quit  C:Clear", (frame.shape[1] - 200, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    cv2.imshow('Sign to Text', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('c'):
        sentence = ""
        current_char = ""
        char_count = 0

cap.release()
cv2.destroyAllWindows()
hand_landmarker.close()

if sentence.strip():
    print(f"Final sentence: {sentence.strip()}")

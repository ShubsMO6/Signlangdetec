import cv2
import numpy as np
from collections import deque
from mediapipe_utils import mp_detection, draw_landmarks, extract_keypoints
from visualization import prob_viz
from model import load_gesture_model, predict_action
import mediapipe as mp
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

actions = ['hello', 'thanks', 'i love you']
colors = [(245, 117, 16), (117, 245, 16), (16, 117, 245)]
seq_length = 30
model = load_gesture_model('action.keras')
sequence = deque(maxlen=seq_length)
sentence = []
threshold = 0.8
cap = cv2.VideoCapture(1)

with mp.solutions.holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame is None:
            break
        image, results = mp_detection(frame, holistic)
        mp.solutions.drawing_utils.draw_landmarks(image, results)
        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        if len(sequence) == seq_length:
            res, action = predict_action(model, list(sequence), actions)
            if res[np.argmax(res)] > threshold and (not sentence or sentence[-1] != action):
                sentence.append(action)
            sentence = sentence[-5:]
            image = prob_viz(res, actions, image, colors)
        cv2.putText(image, ' '.join(sentence), (3, 30), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow('Sign Language Detection', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()

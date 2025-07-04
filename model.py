import numpy as np
from tensorflow.keras.models import load_model

def load_gesture_model(model_path='action.keras'):
    return load_model(model_path)

def predict_action(model, sequence, actions):
    res = model.predict(np.expand_dims(sequence, axis=0))[0]
    idx = np.argmax(res)
    return res, actions[idx]
import cv2

def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    for i, prob in enumerate(res):
        cv2.rectangle(output_frame, (0, 60 + i * 40), (int(prob * 100), 90 + i * 40), colors[i], -1)
        cv2.putText(output_frame, actions[i], (0, 85 + i * 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    return output_frame
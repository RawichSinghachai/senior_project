import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Global zoom settings
zoom_factor = 1.0
zoom_step = 0.1
zoom_max = 3.0
zoom_min = 1.0

def get_hand_side(wrist_x, image_width):
    return "Left Hand" if wrist_x < image_width / 2 else "Right Hand"

def check_hand_orientation(landmarks, hand_side):
    palm_center = landmarks[9]
    thumb = landmarks[4]

    if hand_side == "Left Hand":
        return "Front (Palm)" if thumb.x > palm_center.x else "Back (Dorsal)"
    else:
        return "Front (Palm)" if thumb.x < palm_center.x else "Back (Dorsal)"

def apply_image_processing(frame):
    contrast = cv2.getTrackbarPos("Contrast", "Hand Detection")
    brightness = cv2.getTrackbarPos("Brightness", "Hand Detection")
    threshold_value = cv2.getTrackbarPos("Threshold", "Hand Detection")
    blur_value = cv2.getTrackbarPos("GaussianBlur", "Hand Detection")

    # Apply contrast and brightness adjustments
    alpha = contrast / 10.0  
    beta = brightness - 50  
    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, thresholded = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    # Apply Gaussian blur
    blur_value = max(1, blur_value // 2 * 2 + 1)
    blurred = cv2.GaussianBlur(thresholded, (blur_value, blur_value), 0)

    return blurred

def zoom_image(frame):
    global zoom_factor
    h, w, _ = frame.shape
    cx, cy = w // 2, h // 2

    new_w = int(w / zoom_factor)
    new_h = int(h / zoom_factor)
    x1, y1 = max(0, cx - new_w // 2), max(0, cy - new_h // 2)
    x2, y2 = min(w, cx + new_w // 2), min(h, cy + new_h // 2)

    cropped = frame[y1:y2, x1:x2]
    return cv2.resize(cropped, (w, h))

def mouse_event(event, x, y, flags, param):
    global zoom_factor
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            zoom_factor = min(zoom_factor + zoom_step, zoom_max)
        else:
            zoom_factor = max(zoom_factor - zoom_step, zoom_min)

def process_camera(frame, hands):
    frame = cv2.flip(frame, 1)
    frame = zoom_image(frame)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            wrist_x = hand_landmarks.landmark[0].x * frame.shape[1]
            hand_side = get_hand_side(wrist_x, frame.shape[1])
            orientation = check_hand_orientation(hand_landmarks.landmark, hand_side)

            h, w, _ = frame.shape
            cx, cy = int(hand_landmarks.landmark[0].x * w), int(hand_landmarks.landmark[0].y * h)
            label = f"{hand_side}: {orientation}"
            cv2.putText(frame, label, (cx, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

    # Display zoom level
    cv2.putText(frame, f"Zoom: {zoom_factor:.1f}x", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    return frame

def main():
    global zoom_factor

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open the webcam.")
        return

    cv2.namedWindow("Hand Detection")
    cv2.setMouseCallback("Hand Detection", mouse_event)

    # Create trackbars
    cv2.createTrackbar("Contrast", "Hand Detection", 10, 30, lambda x: None)
    cv2.createTrackbar("Brightness", "Hand Detection", 50, 100, lambda x: None)
    cv2.createTrackbar("Threshold", "Hand Detection", 128, 255, lambda x: None)
    cv2.createTrackbar("GaussianBlur", "Hand Detection", 5, 25, lambda x: None)

    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read a frame from the webcam.")
                break

            processed_frame = process_camera(frame, hands)
            filtered_frame = apply_image_processing(processed_frame)

            # Merge original and processed frames
            merged = cv2.addWeighted(processed_frame, 0.7, cv2.cvtColor(filtered_frame, cv2.COLOR_GRAY2BGR), 0.3, 0)

            cv2.imshow("Hand Detection", merged)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

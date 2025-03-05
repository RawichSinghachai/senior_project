import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands and drawing tools
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Global variables for zoom
zoom_factor = 1.0
zoom_step = 0.1
zoom_center = (0, 0)

# Function to determine left or right hand
def get_hand_side(wrist_x, image_width):
    return "Left Hand" if wrist_x < image_width / 2 else "Right Hand"

# Function to determine if hand is front or back
def check_hand_orientation(landmarks, hand_side):
    palm_center = landmarks[9]
    thumb = landmarks[4]

    if hand_side == "Left Hand":
        return "Front (Palm)" if thumb.x > palm_center.x else "Back (Dorsal)"
    else:
        return "Front (Palm)" if thumb.x < palm_center.x else "Back (Dorsal)"

def apply_image_processing(frame):
    """
    Applies brightness/contrast adjustment, thresholding, and Gaussian blur based on trackbar values.
    """
    alpha = cv2.getTrackbarPos("Alpha", "Hand Detection") / 100
    beta = cv2.getTrackbarPos("Beta", "Hand Detection") - 100
    threshold_value = cv2.getTrackbarPos("Threshold", "Hand Detection")
    blur_value = cv2.getTrackbarPos("GaussianBlur", "Hand Detection")

    # Apply brightness and contrast
    adjusted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    # Convert to grayscale and apply threshold
    gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    # Apply Gaussian Blur (must be odd number)
    blur_value = max(1, blur_value // 2 * 2 + 1)
    blurred = cv2.GaussianBlur(thresholded, (blur_value, blur_value), 0)

    return blurred

def zoom_image(frame):
    global zoom_factor, zoom_center
    h, w, _ = frame.shape

    # Define zoom center (middle of frame)
    cx, cy = w // 2, h // 2

    # Define zoomed ROI
    new_w = int(w / zoom_factor)
    new_h = int(h / zoom_factor)
    x1, y1 = max(0, cx - new_w // 2), max(0, cy - new_h // 2)
    x2, y2 = min(w, cx + new_w // 2), min(h, cy + new_h // 2)

    # Crop and resize
    cropped = frame[y1:y2, x1:x2]
    return cv2.resize(cropped, (w, h))

def mouse_event(event, x, y, flags, param):
    global zoom_factor
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            zoom_factor = min(zoom_factor + zoom_step, 3.0)
        else:
            zoom_factor = max(zoom_factor - zoom_step, 1.0)

def process_camera(frame, hands):
    """
    Processes the camera frame, detects hands, determines hand side and orientation,
    and draws landmarks and labels.
    """
    frame = cv2.flip(frame, 1)  # Flip for a mirror effect
    frame = zoom_image(frame)  # Apply zoom

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
    cv2.createTrackbar("Alpha", "Hand Detection", 100, 300, lambda x: None)
    cv2.createTrackbar("Beta", "Hand Detection", 100, 200, lambda x: None)
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

            cv2.imshow("Hand Detection", processed_frame)
            cv2.imshow("Processed", filtered_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

import cv2
import mediapipe as mp

# Initialize MediaPipe Hands and drawing tools
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Function to determine left or right hand
def get_hand_side(wrist_x, image_width):
    if wrist_x < image_width / 2:
        return "Left Hand"
    else:
        return "Right Hand"

# Function to determine if hand is front or back with left-right distinction
def check_hand_orientation(landmarks, hand_side):
    palm_center = landmarks[9]
    thumb = landmarks[4]
    pinky = landmarks[20]

    # Check thumb relative position depending on hand side
    if hand_side == "Left Hand":
        if thumb.x > palm_center.x:
            return "Front (Palm)"
        else:
            return "Back (Dorsal)"
    else:
        if thumb.x < palm_center.x:
            return "Front (Palm)"
        else:
            return "Back (Dorsal)"

def process_camera(frame, hands):
    """
    Processes the camera frame, detects hands, determines hand side and orientation,
    and draws landmarks and labels.
    """
    # Flip the image horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and detect hand landmarks
    results = hands.process(frame_rgb)

    # Draw landmarks and check hand orientation for each detected hand
    if results.multi_hand_landmarks:
        for hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Draw hand landmarks on the image
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Determine hand side (left or right)
            wrist_x = hand_landmarks.landmark[0].x * frame.shape[1]
            hand_side = get_hand_side(wrist_x, frame.shape[1])

            # Determine orientation (front or back) with respect to hand side
            orientation = check_hand_orientation(hand_landmarks.landmark, hand_side)

            # Display information near the detected hand
            h, w, _ = frame.shape
            cx, cy = int(hand_landmarks.landmark[0].x * w), int(hand_landmarks.landmark[0].y * h)
            label = f"{hand_side}: {orientation}"
            cv2.putText(frame, label, (cx, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

    return frame

def main():
    """
    Main function to run the camera and process frames in real-time.
    """
    # Open the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open the webcam.")
        return

    # Initialize MediaPipe Hands
    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read a frame from the webcam.")
                break

            # Process the frame and get the result
            processed_frame = process_camera(frame, hands)

            # Display the result
            cv2.imshow('Hand Detection', processed_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

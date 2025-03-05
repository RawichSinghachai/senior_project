import cv2
import mediapipe as mp
import time
import os
from utils.arduino import ArduinoController
from utils.logger import AppLogger

logger = AppLogger().get_logger()

# Initialize MediaPipe Hands and drawing tools
hand_data = {"Left Hand": None, "Right Hand": None}
mp_hands = mp.solutions.hands

def get_hand_side(wrist_x, image_width):
    return "Left Hand" if wrist_x < image_width / 2 else "Right Hand"

def check_hand_orientation(landmarks, hand_side):
    palm_center = landmarks[9]
    thumb = landmarks[4]
    
    if hand_side == "Left Hand":
        return "Front (Palm)" if thumb.x > palm_center.x else "Back (Dorsal)"
    else:
        return "Front (Palm)" if thumb.x < palm_center.x else "Back (Dorsal)"

def zoom_frame(frame, zoom_factor=1.2):
    height, width, _ = frame.shape
    new_width = int(width / zoom_factor)
    new_height = int(height / zoom_factor)
    x1 = (width - new_width) // 2
    y1 = (height - new_height) // 2
    x2 = x1 + new_width
    y2 = y1 + new_height
    cropped = frame[y1:y2, x1:x2]
    return cv2.resize(cropped, (width, height))

def process_camera(frame, hands, countdown, i, blur_value=5, threshold_value=50, contrast=0, brightness=0):

    frame = cv2.flip(frame, -1)
    
    frame = zoom_frame(frame)
    blur_value = (blur_value * 2) + 1  
    alpha = contrast / 10.0  
    beta = brightness - 50  

    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
    ImageLAB = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)[:, :, 0]
    blur = cv2.GaussianBlur(ImageLAB, (blur_value, blur_value), 0)
    _, binary = cv2.threshold(blur, threshold_value, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    left_hand_area = 0
    right_hand_area = 0
    image_center_x = frame.shape[1] // 2

    cv2.line(frame, (image_center_x, 0), (image_center_x, frame.shape[0]), (0, 0, 255), 2)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:
            contour_center_x = cv2.boundingRect(contour)[0] + cv2.boundingRect(contour)[2] // 2
            if contour_center_x < image_center_x:
                left_hand_area += area
            else:
                right_hand_area += area
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

    hand_data["Left Hand"], hand_data["Right Hand"] = None, None
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):
            wrist_x = hand_landmarks.landmark[0].x * frame.shape[1]
            hand_side = get_hand_side(wrist_x, frame.shape[1])
            orientation = check_hand_orientation(hand_landmarks.landmark, hand_side)
            hand_data[hand_side] = orientation
            hand_text = f"{hand_side}: {orientation}"

    left_hand_status = hand_data["Left Hand"]
    right_hand_status = hand_data["Right Hand"]

    if left_hand_status and right_hand_status:
        if (left_hand_status == "Back (Dorsal)" and right_hand_status == "Front (Palm)") or \
           (left_hand_status == "Front (Palm)" and right_hand_status == "Back (Dorsal)"):
            cv2.putText(frame, "Error: Conflicting Hand Orientation", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.putText(frame, f"Countdown: {countdown}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Round : {i+1}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return frame, left_hand_area, right_hand_area

def main(userId):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.error("Could not open the webcam.")
        return None, "Could not open the webcam."

    arduino = ArduinoController()
    arduino.connect()
    
    snapshot_folder = "snapshots"
    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder)

    video_folder = os.path.join("video", str(userId))
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    video_filename = os.path.join(video_folder, f"{timestamp}.mp4")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = None  
    recording = False  

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) 

    time_countdown = [5,5,5,5]
    wait_time = [2,2,2]
    parameters = [
        {"threshold": 74, "blur": 2, "brightness": 25, "contrast": 7},
        {"threshold": 74, "blur": 2, "brightness": 25, "contrast": 7},
        {"threshold": 50, "blur": 2, "brightness": 29, "contrast": 7},
        {"threshold": 75, "blur": 2, "brightness": 29, "contrast": 7},
    ]

    try:
        with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:
            for i in range(len(time_countdown)):
                ret, frame = cap.read()
                frame = zoom_frame(frame)
                if recording:
                    video_writer.write(frame)
    
    except Exception as e:
        logger.error(f"An error occurred in computer vision : {e}")
        return None, str(e)
    
    finally:
        if recording and video_writer is not None:
            video_writer.release()
        arduino.send_command("off")
        arduino.close_connection()
        cap.release()
        cv2.destroyAllWindows()

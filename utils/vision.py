import cv2
import mediapipe as mp
import time
# from utils.arduino import ArduinoController

# Initialize MediaPipe Hands and drawing tools
hand_data = {"Left Hand": None, "Right Hand": None}

mp_hands = mp.solutions.hands


def get_hand_side(wrist_x, image_width):
    if wrist_x < image_width / 2:
        return "Left Hand"
    else:
        return "Right Hand"

def check_hand_orientation(landmarks, hand_side):
    palm_center = landmarks[9]
    thumb = landmarks[4]
    pinky = landmarks[20]

    if hand_side == "Left Hand":
        return "Front (Palm)" if thumb.x > palm_center.x else "Back (Dorsal)"
    else:
        return "Front (Palm)" if thumb.x < palm_center.x else "Back (Dorsal)"

def process_camera(frame, hands, countdown, position, callback, blur_value=5, threshold_value=50, contrast=0, brightness=0):
    blur_value  = (blur_value * 2) + 1 
    alpha = contrast / 10.0  
    beta = brightness - 50 

    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
    ImageLAB = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)[:, :, 0]
    blur = cv2.GaussianBlur(ImageLAB, (blur_value, blur_value), 0)
    _, binary = cv2.threshold(blur, threshold_value, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    left_hand_area = right_hand_area = 0
    image_center_x = frame.shape[1] // 2

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
            cv2.putText(frame, hand_text, (10, 100 + 50 * hand_index), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    callback(hand_data)

    x, y = position
    cv2.putText(frame, f"Countdown: {countdown}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    return frame, left_hand_area, right_hand_area

def main(callback, result_callback):
    # arduino = ArduinoController()
    # arduino.connect()
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open the webcam.")
        return
    
    
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

    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:
        sum_areas = []
        for i in range(len(time_countdown)):
            countdown = time_countdown[i]
            start_time = time.time()
            param = parameters[i]
            position = (50, 50)

            while countdown > 0:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read a frame from the webcam.")
                    break
                if time.time() - start_time >= 1:
                    countdown -= 1
                    start_time = time.time()

                processed_frame, left_hand_area, right_hand_area = process_camera(
                    frame, hands, countdown, position,callback,
                    blur_value=param["blur"], threshold_value=param["threshold"],
                    contrast=param["contrast"], brightness=param["brightness"]
                )
                cv2.putText(processed_frame, f"Left Hand Area: {left_hand_area}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(processed_frame, f"Right Hand Area: {right_hand_area}", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.namedWindow("Webcam", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("Webcam", cv2.WND_PROP_TOPMOST, 1)
                cv2.imshow('Webcam', processed_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return

            sum_areas.append({"left_hand_area": left_hand_area, "right_hand_area": right_hand_area})
            if i < len(wait_time):
                print(f"Waiting for {wait_time[i]} seconds...")
                time.sleep(wait_time[i])

        print("All countdowns completed.")
        print("Hand areas:", sum_areas)

    cap.release()
    cv2.destroyAllWindows()
    result_callback(sum_areas)



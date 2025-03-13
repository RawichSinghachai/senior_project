import cv2
import mediapipe as mp
import time
import os
from utils.arduino import ArduinoController
from utils.logger import AppLogger

logger = AppLogger.get_logger()

# Initialize MediaPipe Hands and drawing tools
hand_data = {"Left Hand": None, "Right Hand": None}
mp_hands = mp.solutions.hands
width, height = 640, 480
center_x = width // 2
left_center_x = center_x // 2
right_center_x = center_x + (center_x // 2)
y_position = 50

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

    # frame = cv2.flip(frame, -1)

    frame = zoom_frame(frame)

    blur_value = (blur_value * 2) + 1  
    alpha = contrast / 10.0  
    beta = brightness - 50  

    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
    ImageLAB = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    if i == 2:
        channel_B = ImageLAB[:, :, 2]  # à¹ƒà¸Šà¹‰à¸Šà¹ˆà¸­à¸‡ B à¹à¸—à¸™ L
        clahe = cv2.createCLAHE(clipLimit=8, tileGridSize=(2, 2))
        processed_channel = clahe.apply(channel_B)
    elif i == 3:
        channel_B = ImageLAB[:, :, 2]  # à¹ƒà¸Šà¹‰à¸Šà¹ˆà¸­à¸‡ B à¹à¸—à¸™ L
        clahe = cv2.createCLAHE(clipLimit=0.1, tileGridSize=(2, 2))
        processed_channel = clahe.apply(channel_B)
    else:
        processed_channel = ImageLAB[:, :, 0]  # à¹ƒà¸Šà¹‰à¸Šà¹ˆà¸­à¸‡ L à¸ªà¸³à¸«à¸£à¸±à¸šà¸£à¸­à¸šà¸—à¸µà¹ˆ 1, 2

    blur = cv2.GaussianBlur(processed_channel, (blur_value, blur_value), 0)
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
           


    # **Check for errors if left and right hands are in a conflicting state**
    left_hand_status = hand_data["Left Hand"]
    right_hand_status = hand_data["Right Hand"]

    # Show hand status on the frame  
    cv2.putText(frame, str(left_hand_status), (left_center_x - 30, y_position), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, str(right_hand_status), (right_center_x - 30, y_position), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

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
        logger.error("Could not open the webcam.") # Log
        return None, "Could not open the webcam."

    # Connect Arduino
    arduino = ArduinoController()
    arduino.connect()
    
    
    
    # à¸ªà¸£à¹‰à¸²à¸‡à¹‚à¸Ÿà¸¥à¹€à¸”à¸­à¸£à¹Œ snapshots à¸–à¹‰à¸²à¸¢à¸±à¸‡à¹„à¸¡à¹ˆà¸¡à¸µ
    snapshot_folder = "snapshots"
    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder)

    video_folder = os.path.join("video", str(userId))
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    # à¸•à¸±à¹‰à¸‡à¸„à¹ˆà¸²à¸‚à¸™à¸²à¸”à¸§à¸´à¸”à¸µà¹‚à¸­
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    video_filename = os.path.join(video_folder, f"{timestamp}.mp4")

    # à¸•à¸±à¹‰à¸‡à¸„à¹ˆà¸²à¸•à¸±à¸§à¸šà¸±à¸™à¸—à¸¶à¸à¸§à¸´à¸”à¸µà¹‚à¸­ (MP4 Codec)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = None  
    recording = False  

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, height) 
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, width) 

    time_countdown = [5,5,5,5]
    wait_time = [2,2,2]
    parameters = [
        {"threshold": 90, "blur": 2, "brightness": 50, "contrast": 9},
        {"threshold": 90, "blur": 2, "brightness": 50, "contrast": 9},
        {"threshold": 121, "blur": 2, "brightness": 100, "contrast": 50},
        {"threshold": 90, "blur": 2, "brightness": 81, "contrast": 34},
    ]

    try:
        with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:
            sum_areas = []
            
            for i in range(len(time_countdown)):
                countdown = time_countdown[i]
                start_time = time.time()
                param = parameters[i]

                if i >= 2:
                    arduino.send_command("on")
                else:
                    arduino.send_command("off")
                    

                while countdown > 0:
                    ret, frame = cap.read()
                    if not ret:
                        logger.error("Could not read a frame from the webcam.") # Log
                        return None, "Error: Could not read a frame from the webcam."
                    if time.time() - start_time >= 1:
                        countdown -= 1
                        start_time = time.time()

                    processed_frame, left_hand_area, right_hand_area = process_camera(
                        frame, hands, countdown, i, 
                        blur_value=param["blur"], threshold_value=param["threshold"],
                        contrast=param["contrast"], brightness=param["brightness"]
                    )
                    
                    if recording:
                        video_writer.write(processed_frame)


                    cv2.imshow('Webcam', processed_frame)


                    # # Move window to the center of the screen
                    # screen_width = 1920  # Adjust to actual screen width
                    # screen_height = 1080 # Adjust to actual screen height
                    # window_height, window_width, _  = frame.shape
                    # cv2.moveWindow('Webcam', (screen_width - window_width) // 2, (screen_height - window_height) // 2)

                    key = cv2.waitKey(1) & 0xFF

                    if key == ord('q'):
                        logger.info("User terminated the process.") # Log
                        return None, "User terminated the process."
                    elif key == ord('r'):  
                        if not recording:
                            video_writer = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame_width, frame_height))
                            logger.info(f"Starting to record video to path: {video_filename}") # Log
                            recording = True
                        else:
                            recording = False
                            video_writer.release()
                            logger.info(f"Stop recording video saved to path : {video_filename}") # Log


                #  Check for conflicting hand orientation each round
                # if i == 0 and not (hand_data["Left Hand"] == "Back (Dorsal)" and hand_data["Right Hand"] == "Back (Dorsal)"):
                #     return None, "fail round 1"
                # if i == 1 and not (hand_data["Left Hand"] == "Front (Palm)" and hand_data["Right Hand"] == "Front (Palm)"):
                #     return None, "fail round 2"
                # if i == 2 and not (hand_data["Left Hand"] == "Back (Dorsal)" and hand_data["Right Hand"] == "Back (Dorsal)"):
                #     return None, "fail round 3"
                # if i == 3 and not (hand_data["Left Hand"] == "Front (Palm)" and hand_data["Right Hand"] == "Front (Palm)"):
                #     return None, "fail round 4"

                #  Check for conflicting hand orientation
                if (hand_data["Left Hand"] == "Back (Dorsal)" and hand_data["Right Hand"] == "Front (Palm)") or \
                    (hand_data["Left Hand"] == "Front (Palm)" and hand_data["Right Hand"] == "Back (Dorsal)"):
                    logger.error("Conflicting Hand Orientation") # Log
                    return None, "Conflicting Hand Orientation"

                # Snapshot
                user_folder = os.path.join(snapshot_folder, str(userId))
                if not os.path.exists(user_folder):
                    os.makedirs(user_folder)

                # Frame Snapshot 
                if i == 2: # B Channel Color round 3 (i == 2)
                    frame = cv2.convertScaleAbs(frame, alpha=5.0, beta=50)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
                    b_channel = frame[:, :, 2]
                    clahe = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(2, 2))
                    snapshot_frame = clahe.apply(b_channel)
                elif i == 3: # B Channel Color round 4 (i == 3)
                    frame = cv2.convertScaleAbs(frame, alpha=5.0, beta=50)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
                    b_channel = frame[:, :, 2]
                    clahe = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(2, 2))
                    snapshot_frame = clahe.apply(b_channel)
                else:
                    snapshot_frame = frame

                snapshot_path = os.path.join(user_folder, f"step_{i}_{timestamp}.jpg")
                cv2.imwrite(snapshot_path, snapshot_frame)
                logger.info(f"Saved snapshot: {snapshot_path}") # Log

                sum_areas.append({"left_hand_area": left_hand_area, "right_hand_area": right_hand_area})
                
                if i < len(wait_time):
                    time.sleep(wait_time[i])

            logger.info(f"UserId : {userId} Process completed.") # Log
            return sum_areas, None
        
    except Exception as e:
        logger.error(f"An error occurred in computer vision : {e}") # Log
        return None, str(e)
    
    finally:
        if recording and video_writer is not None:
            video_writer.release()
            logger.info(f"Stop recording video saved to path: {video_filename}") # Log
        arduino.send_command("off")
        arduino.close_connection()
        
        cap.release()
        cv2.destroyAllWindows()
        logger.info("Camera released and windows closed.") # Log

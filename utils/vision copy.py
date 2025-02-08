import cv2
import mediapipe as mp
import time
# from utils.controlRelay import active_relay,deactive_relay

# Initialize MediaPipe Hands and drawing tools
hand_data = {"Left Hand": None, "Right Hand": None}

mp_hands = mp.solutions.hands

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

def process_camera(frame, hands, countdown, position, blur_value=5, threshold_value=50, contrast=0, brightness=0):
    """
    Processes the camera frame, detects hands, determines hand side and orientation,
    and applies contour detection.
    """

    alpha = contrast / 10.0  
    beta = brightness - 50 

    # Convert the BGR image to LAB and process it
    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
    ImageLAB = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    ImageLAB = ImageLAB[:, :, 0]
    blur = cv2.GaussianBlur(ImageLAB, (blur_value, blur_value), 0)
    _, binary = cv2.threshold(blur, threshold_value, 255, cv2.THRESH_BINARY)

    # Find contours in the mask
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    left_hand_area = 0
    right_hand_area = 0
    image_center_x = frame.shape[1] // 2  # Center of the image width

    for contour in contours:
        # Filter out small contours based on area
        area = cv2.contourArea(contour)
        if area > 500:
            contour_center_x = cv2.boundingRect(contour)[0] + cv2.boundingRect(contour)[2] // 2
            if contour_center_x < image_center_x:
                left_hand_area += area
            else:
                right_hand_area += area
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

    # Reset hand data
    hand_data["Left Hand"], hand_data["Right Hand"] = None, None

    # Process the image for hand detection (no skeleton drawn)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Determine hand side (left or right)
            wrist_x = hand_landmarks.landmark[0].x * frame.shape[1]
            hand_side = get_hand_side(wrist_x, frame.shape[1])

            # Determine orientation (front or back) with respect to hand side
            orientation = check_hand_orientation(hand_landmarks.landmark, hand_side)

            # Update hand data
            hand_data[hand_side] = orientation

            # Display hand side and orientation
            hand_text = f"{hand_side}: {orientation}"
            cv2.putText(frame, hand_text, (10, 100 + 50 * hand_index), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the countdown number at the specified position
    x, y = position
    countdown_text = f"Countdown: {countdown}"
    cv2.putText(frame, countdown_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    return frame, left_hand_area, right_hand_area

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
        total_countdowns = 4
        countdown_duration = 10
        wait_duration = 5
        sum_areas = []

        for i in range(total_countdowns):
            # Control Relay
            # if i >= 2:
            #     active_relay()
            # else:
            #     deactive_relay()
            countdown = countdown_duration
            start_time = time.time()

            # Set the position for the countdown text
            position = (50, 50)  # Top-left corner of the screen

            while countdown > 0:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read a frame from the webcam.")
                    break

                # Update countdown timer
                elapsed_time = time.time() - start_time
                if elapsed_time >= 1:
                    countdown -= 1
                    start_time = time.time()

                # Process the frame and get the result
                processed_frame, left_hand_area, right_hand_area = process_camera(frame, hands, countdown, position)

                # Display the hand areas
                cv2.putText(processed_frame, f"Left Hand Area: {left_hand_area}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(processed_frame, f"Right Hand Area: {right_hand_area}", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Display the result
                cv2.imshow('Webcam', processed_frame)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return

            # Append the areas for this countdown to the list
            sum_areas.append({
                "left_hand_area": left_hand_area,
                "right_hand_area": right_hand_area
            })



            # Wait for 5 seconds before the next countdown
            if i < total_countdowns - 1:
                print("Waiting for 5 seconds...")
                time.sleep(wait_duration)

        print("All countdowns completed.")
        print("Hand areas:", sum_areas)

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    return sum_areas

main()
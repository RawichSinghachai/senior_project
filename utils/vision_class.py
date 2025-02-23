import cv2
import mediapipe as mp
import time
import os
from utils.logger import AppLogger

class HandTrackingProcessor:
    def __init__(self, userId):
        self.logger = AppLogger().get_logger()
        self.userId = userId
        self.cap = cv2.VideoCapture(0)
        self.hand_data = {"Left Hand": None, "Right Hand": None}
        self.mp_hands = mp.solutions.hands
        self.recording = False
        self.video_writer = None
        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))
        self.snapshot_folder = "snapshots"
        self.video_folder = "video"
        self.video_filename = os.path.join(self.video_folder, f"recorded_video_{userId}.avi")
        self.time_countdown = [5, 5, 5, 5]
        self.wait_time = [2, 2, 2]
        self.parameters = [
            {"threshold": 74, "blur": 2, "brightness": 25, "contrast": 7},
            {"threshold": 74, "blur": 2, "brightness": 25, "contrast": 7},
            {"threshold": 50, "blur": 2, "brightness": 29, "contrast": 7},
            {"threshold": 75, "blur": 2, "brightness": 29, "contrast": 7},
        ]
        self._setup()

    def _setup(self):
        if not os.path.exists(self.snapshot_folder):
            os.makedirs(self.snapshot_folder)
        if not os.path.exists(self.video_folder):
            os.makedirs(self.video_folder)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def get_hand_side(self, wrist_x, image_width):
        return "Left Hand" if wrist_x < image_width / 2 else "Right Hand"

    def check_hand_orientation(self, landmarks, hand_side):
        palm_center = landmarks[9]
        thumb = landmarks[4]
        return "Front (Palm)" if (thumb.x > palm_center.x if hand_side == "Left Hand" else thumb.x < palm_center.x) else "Back (Dorsal)"

    def process_camera(self, frame, hands, countdown, i, blur_value=5, threshold_value=50, contrast=0, brightness=0):
        blur_value = (blur_value * 2) + 1  
        alpha = contrast / 10.0  
        beta = brightness - 50  
        frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
        ImageLAB = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)[:, :, 0]
        blur = cv2.GaussianBlur(ImageLAB, (blur_value, blur_value), 0)
        _, binary = cv2.threshold(blur, threshold_value, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        left_hand_area, right_hand_area = 0, 0
        image_center_x = frame.shape[1] // 2
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                contour_center_x = cv2.boundingRect(contour)[0] + cv2.boundingRect(contour)[2] // 2
                (left_hand_area if contour_center_x < image_center_x else right_hand_area) += area
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
        self.hand_data["Left Hand"], self.hand_data["Right Hand"] = None, None
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                wrist_x = hand_landmarks.landmark[0].x * frame.shape[1]
                hand_side = self.get_hand_side(wrist_x, frame.shape[1])
                self.hand_data[hand_side] = self.check_hand_orientation(hand_landmarks.landmark, hand_side)
        return frame, left_hand_area, right_hand_area

    def run(self):
        try:
            with self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:
                sum_areas = []
                for i, countdown in enumerate(self.time_countdown):
                    param = self.parameters[i]
                    start_time = time.time()
                    while countdown > 0:
                        ret, frame = self.cap.read()
                        if not ret:
                            return None, "Error: Could not read a frame from the webcam."
                        if time.time() - start_time >= 1:
                            countdown -= 1
                            start_time = time.time()
                        processed_frame, left_hand_area, right_hand_area = self.process_camera(
                            frame, hands, countdown, i, **param)
                        if self.recording:
                            self.video_writer.write(processed_frame)
                        cv2.imshow('Webcam', processed_frame)
                        key = cv2.waitKey(1) & 0xFF
                        if key == ord('q'):
                            return None, "User terminated the process."
                        elif key == ord('r'):
                            self.toggle_recording()
                    if self.hand_data["Left Hand"] and self.hand_data["Right Hand"] and (
                        self.hand_data["Left Hand"] != self.hand_data["Right Hand"]):
                        return None, "Conflicting Hand Orientation"
                    self.save_snapshot(i, processed_frame)
                    sum_areas.append({"left_hand_area": left_hand_area, "right_hand_area": right_hand_area})
                    if i < len(self.wait_time):
                        time.sleep(self.wait_time[i])
                return sum_areas, None
        finally:
            self.cleanup()

    def toggle_recording(self):
        if not self.recording:
            self.video_writer = cv2.VideoWriter(self.video_filename, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (self.frame_width, self.frame_height))
            self.recording = True
        else:
            self.recording = False
            self.video_writer.release()

    def save_snapshot(self, step, frame):
        user_folder = os.path.join(self.snapshot_folder, str(self.userId))
        os.makedirs(user_folder, exist_ok=True)
        snapshot_path = os.path.join(user_folder, f"step_{step}_{time.strftime('%Y%m%d_%H%M%S')}.jpg")
        cv2.imwrite(snapshot_path, frame)

    def cleanup(self):
        if self.recording:
            self.video_writer.release()
        self.cap.release()
        cv2.destroyAllWindows()

# Example usage:
# processor = HandTrackingProcessor(userId=123)
# result, error = processor.run()
# print(result, error)

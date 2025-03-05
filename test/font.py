import sys
import cv2
import mediapipe as mp
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal

# === MediaPipe Hand Detection ===
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


class HandDetectionThread(QThread):
    hand_signal = pyqtSignal(str, str)  # ส่งค่า (left_hand_text, right_hand_text)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(0)  # เปิดกล้อง
        with mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as hands:
            while self.running:
                ret, frame = cap.read()
                if not ret:
                    continue

                # แปลงเป็น RGB และตรวจจับมือ
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb_frame)

                left_hand_text = "No Left Hand"
                right_hand_text = "No Right Hand"

                if results.multi_hand_landmarks:
                    for hand_landmarks, hand_info in zip(results.multi_hand_landmarks, results.multi_handedness):
                        hand_label = hand_info.classification[0].label  # "Left" or "Right"

                        # จุด Landmark
                        wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

                        # คำนวณการวางมือ (Front หรือ Back)
                        if wrist.z < index_tip.z and wrist.z < pinky_tip.z:
                            hand_position = "Front Hand"
                        else:
                            hand_position = "Back Hand"

                        if hand_label == "Left":
                            left_hand_text = f"Left: {hand_position}"
                        else:
                            right_hand_text = f"Right: {hand_position}"

                        # วาดเส้นบนมือ
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # ส่งข้อมูลไป PyQt6
                self.hand_signal.emit(left_hand_text, right_hand_text)

                # แสดง OpenCV
                cv2.imshow("Hand Detection", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


# === PyQt6 GUI ===
class HandDisplayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hand Tracking Info")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()
        self.left_hand_label = QLabel("Left: Waiting...")
        self.right_hand_label = QLabel("Right: Waiting...")

        self.layout.addWidget(self.left_hand_label)
        self.layout.addWidget(self.right_hand_label)
        self.setLayout(self.layout)

        # เรียกใช้ Thread ตรวจจับมือ
        self.hand_thread = HandDetectionThread()
        self.hand_thread.hand_signal.connect(self.update_hand_labels)
        self.hand_thread.start()

    def update_hand_labels(self, left_text, right_text):
        self.left_hand_label.setText(left_text)
        self.right_hand_label.setText(right_text)

    def closeEvent(self, event):
        self.hand_thread.stop()
        event.accept()


# === Start PyQt Application ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HandDisplayWindow()
    window.show()
    sys.exit(app.exec())

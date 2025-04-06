from PyQt6.QtCore import Qt , QSize
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,QHBoxLayout)
import cv2
from utils.arduino import ArduinoController

def nothing(x):
    pass

def vision():
    # เปิดกล้อง
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # สร้าง Trackbar
    cv2.namedWindow("Controls")
    cv2.createTrackbar("Threshold", "Controls", 100, 255, nothing)
    cv2.createTrackbar("Blur", "Controls", 1, 20, nothing)
    cv2.createTrackbar("Brightness", "Controls", 50, 100, nothing)
    cv2.createTrackbar("Contrast", "Controls", 10, 20, nothing)
    cv2.createTrackbar("ClipLimit", "Controls", 10, 100, nothing)
    cv2.createTrackbar("TileSize", "Controls", 1, 32, nothing)

    # ตัวแปรสำหรับการสลับโหมด
    show_binary = False  # เริ่มต้นเป็น RGB
    show_b_channel = False  # โหมด B Channel

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # รับค่าจาก Trackbar
        threshold_value = cv2.getTrackbarPos("Threshold", "Controls")
        blur_value = cv2.getTrackbarPos("Blur", "Controls")
        brightness = cv2.getTrackbarPos("Brightness", "Controls") - 50
        contrast = cv2.getTrackbarPos("Contrast", "Controls") / 10.0  
        clip = cv2.getTrackbarPos("ClipLimit", "Controls") / 10.0
        tile = cv2.getTrackbarPos("TileSize", "Controls")
        tile = max(2, tile)

        blur_value = (blur_value * 2) + 1  # ทำให้ค่าคงเป็นเลขคี่

        # ปรับ Brightness และ Contrast
        frame = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)

        # แปลงเป็น LAB แล้วใช้ B Channel
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l_channel = lab[:, :, 0]  # ช่องที่ 0 คือ L Channel
        b_channel = lab[:, :, 2]  # ช่องที่ 2 คือ B Channel

        # ปรับ Contrast ด้วย CLAHE  cliplimt 1.0-10.0, tile 2-32 (even number)
        clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=(tile, tile))
        b_clahe = clahe.apply(b_channel)

        # ใช้ Gaussian Blur
        blur = cv2.GaussianBlur(b_clahe, (blur_value, blur_value), 0)

        # ใช้ Threshold
        _, binary = cv2.threshold(blur, threshold_value, 255, cv2.THRESH_BINARY)

        # ค้นหา Contour
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

        # เลือกโหมดการแสดงผล
        if show_b_channel:
            display_frame = cv2.cvtColor(b_clahe, cv2.COLOR_GRAY2BGR)
        elif show_binary:
            display_frame = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        else:
            display_frame = frame

        cv2.imshow("Webcam", display_frame)

        # รับค่าจาก Keyboard
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('t'):
            show_binary = not show_binary
        elif key == ord('b'):
            show_b_channel = not show_b_channel

    cap.release()
    cv2.destroyAllWindows()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calibration")
        self.setFixedSize(QSize(800, 400))
        # connect Arduino
        self.arduino = ArduinoController()
        self.arduino.connect()

        # Create layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.hBox_button = QHBoxLayout()
        self.hBox_button.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(self.hBox_button)


        # Create a button
        self.button_camera = QPushButton("Open Camera")
        self.button_camera.clicked.connect(self.on_button_camera)  # Connect button click signal to a slot
        self.hBox_button.addWidget(self.button_camera)

        self.button_on = QPushButton("On")
        self.button_on.clicked.connect(self.on_button_on)  # Connect button click signal to a slot
        self.hBox_button.addWidget(self.button_on)

        self.button_off = QPushButton("Off")
        self.button_off.clicked.connect(self.on_button_off)  # Connect button click signal to a slot
        self.hBox_button.addWidget(self.button_off)


    def on_button_camera(self):
        # Open camera and start vision processing
        vision()

    def on_button_on(self):
        # Perform action when "On" button is clicked
        self.arduino.send_command("on")
        print("On button clicked")
    
    def on_button_off(self):
        # Perform action when "Off" button is clicked
        self.arduino.send_command("off")
        print("Off button clicked")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
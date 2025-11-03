from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
import cv2
from arduino import ArduinoController

# Flags for display mode
show_binary = False
show_b_channel = False

def nothing(x):
    pass

def vision():
    global show_binary, show_b_channel

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    cv2.namedWindow("Controls")
    cv2.createTrackbar("Threshold", "Controls", 100, 255, nothing)
    cv2.createTrackbar("Blur", "Controls", 1, 20, nothing)
    cv2.createTrackbar("Brightness", "Controls", 50, 100, nothing)
    cv2.createTrackbar("Contrast", "Controls", 10, 50, nothing)
    cv2.createTrackbar("ClipLimit", "Controls", 10, 100, nothing)
    cv2.createTrackbar("TileSize", "Controls", 1, 32, nothing)
    
    # ✅ เพิ่ม Trackbar สำหรับ Zoom
    cv2.createTrackbar("Zoom", "Controls", 10, 20, nothing)  # 1.0 - 2.0 (คูณ 10 เพื่อความละเอียด)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        threshold_value = cv2.getTrackbarPos("Threshold", "Controls")
        blur_value = cv2.getTrackbarPos("Blur", "Controls")
        brightness = cv2.getTrackbarPos("Brightness", "Controls") - 50
        contrast = cv2.getTrackbarPos("Contrast", "Controls") / 10.0
        clip = cv2.getTrackbarPos("ClipLimit", "Controls") / 10.0
        tile = max(2, cv2.getTrackbarPos("TileSize", "Controls"))
        zoom_value = cv2.getTrackbarPos("Zoom", "Controls") / 10.0  # ✅ ค่าซูม 1.0–2.0
        blur_value = (blur_value * 2) + 1

        frame = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)

        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        b_channel = lab[:, :, 2]

        clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=(tile, tile))
        b_clahe = clahe.apply(b_channel)

        blur = cv2.GaussianBlur(b_clahe, (blur_value, blur_value), 0)
        _, binary = cv2.threshold(blur, threshold_value, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

        # Display mode selection
        if show_b_channel:
            display_frame = cv2.cvtColor(b_clahe, cv2.COLOR_GRAY2BGR)
        elif show_binary:
            display_frame = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        else:
            display_frame = frame

        # ✅ Apply zoom
        if zoom_value > 1.0:
            h, w = display_frame.shape[:2]
            new_w, new_h = int(w / zoom_value), int(h / zoom_value)
            x1 = (w - new_w) // 2
            y1 = (h - new_h) // 2
            cropped = display_frame[y1:y1 + new_h, x1:x1 + new_w]
            display_frame = cv2.resize(cropped, (w, h))
        
        cv2.imshow("Webcam", display_frame)

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

        self.arduino = ArduinoController()
        self.arduino.connect()

        # Main vertical layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Row 1 - Camera, On, Off
        self.row1 = QHBoxLayout()
        self.row1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(self.row1)

        self.button_camera = QPushButton("Open Camera")
        self.button_camera.clicked.connect(self.on_button_camera)
        self.row1.addWidget(self.button_camera)

        self.button_on = QPushButton("On")
        self.button_on.clicked.connect(self.on_button_on)
        self.row1.addWidget(self.button_on)

        self.button_off = QPushButton("Off")
        self.button_off.clicked.connect(self.on_button_off)
        self.row1.addWidget(self.button_off)

        # Row 2 - Display mode buttons
        self.row2 = QHBoxLayout()
        self.row2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(self.row2)

        self.button_binary = QPushButton("Show Binary")
        self.button_binary.clicked.connect(self.show_binary)
        self.row2.addWidget(self.button_binary)

        self.button_bchannel = QPushButton("Show B Channel")
        self.button_bchannel.clicked.connect(self.show_b_channel)
        self.row2.addWidget(self.button_bchannel)

        self.button_normal = QPushButton("Show Normal")
        self.button_normal.clicked.connect(self.show_normal)
        self.row2.addWidget(self.button_normal)

    def on_button_camera(self):
        vision()

    def on_button_on(self):
        self.arduino.send_command("on")
        print("On button clicked")

    def on_button_off(self):
        self.arduino.send_command("off")
        print("Off button clicked")

    def show_binary(self):
        global show_binary, show_b_channel
        show_binary = True
        show_b_channel = False
        print("Switched to Binary mode")

    def show_b_channel(self):
        global show_binary, show_b_channel
        show_b_channel = True
        show_binary = False
        print("Switched to B Channel mode")

    def show_normal(self):
        global show_binary, show_b_channel
        show_binary = False
        show_b_channel = False
        print("Switched to Normal mode")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

import cv2
import numpy as np

# เปิดเว็บแคม
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("ไม่สามารถเปิดกล้องได้")
    exit()

# ค่าเริ่มต้นของการซูม
zoom_factor = 1.0
zoom_step = 0.1  # ปรับค่าการซูมต่อการ scroll
min_zoom = 1.0   # ไม่ซูม
max_zoom = 3.0   # ซูมมากสุด 3 เท่า

# ฟังก์ชันจัดการ Mouse Scroll เพื่อซูม
def zoom(event, x, y, flags, param):
    global zoom_factor
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:  # Scroll ขึ้น → ซูมเข้า
            zoom_factor = min(zoom_factor + zoom_step, max_zoom)
        else:  # Scroll ลง → ซูมออก
            zoom_factor = max(zoom_factor - zoom_step, min_zoom)

# ตั้งค่า callback สำหรับ mouse scroll
cv2.namedWindow("Webcam Zoom")
cv2.setMouseCallback("Webcam Zoom", zoom)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape  # ขนาดเดิมของเฟรม
    zoom_w, zoom_h = int(w / zoom_factor), int(h / zoom_factor)  # คำนวณขนาด crop

    # คำนวณจุดเริ่มต้นของ crop (เพื่อให้ crop อยู่กึ่งกลางภาพ)
    x1, y1 = (w - zoom_w) // 2, (h - zoom_h) // 2
    x2, y2 = x1 + zoom_w, y1 + zoom_h

    # Crop เฉพาะบริเวณที่ต้องการซูม
    cropped_frame = frame[y1:y2, x1:x2]

    # ปรับขนาดกลับไปเป็นขนาดเดิม
    zoomed_frame = cv2.resize(cropped_frame, (w, h), interpolation=cv2.INTER_CUBIC)

    # แสดงภาพ
    cv2.imshow("Webcam Zoom", zoomed_frame)

    # กด 'q' เพื่อออกจากโปรแกรม
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ปิดการเชื่อมต่อกล้อง
cap.release()
cv2.destroyAllWindows()

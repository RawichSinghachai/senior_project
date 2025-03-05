import cv2
import mediapipe as mp
import numpy as np

# โหลดโมดูล MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# สร้างตัวตรวจจับมือ
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# เปิดกล้อง
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # แปลงสีภาพเป็น RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # วาดจุดเชื่อมต่อของมือ
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # ดึงตำแหน่ง 21 จุดของมือ
            points = [(int(l.x * frame.shape[1]), int(l.y * frame.shape[0])) for l in hand_landmarks.landmark]

            # คำนวณ Convex Hull เพื่อหาขอบเขตของมือ
            hull = cv2.convexHull(np.array(points))
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            cv2.fillConvexPoly(mask, hull, 255)

            # คำนวณพื้นที่ทั้งหมดของมือ
            total_area = np.sum(mask == 255)

            # คำนวณพื้นที่รอบจุดแต่ละจุด
            point_areas = []
            for p in points:
                point_mask = np.zeros_like(mask)
                cv2.circle(point_mask, p, 20, 255, -1)  # วงกลมรอบจุด
                point_area = np.sum((mask == 255) & (point_mask == 255))
                point_areas.append(point_area / total_area * 100)  # เปลี่ยนเป็นเปอร์เซ็นต์

            # แสดงค่าบนหน้าจอ
            for i, (p, area_percent) in enumerate(zip(points, point_areas)):
                cv2.putText(frame, f"{area_percent:.1f}%", (p[0]+5, p[1]-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

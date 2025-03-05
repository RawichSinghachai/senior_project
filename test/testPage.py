import cv2

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open webcam")
    exit()

window_name = "Webcam"
cv2.namedWindow(window_name)  # Create a named window

# Show one frame to get the window size
ret, frame = cap.read()
cv2.imshow(window_name, frame)
cv2.waitKey(1)  # Allow OpenCV to initialize the window

# Get window size
(w_x, w_y, w_w, w_h) = cv2.getWindowImageRect(window_name)

# Calculate center position
screen_w, screen_h = 1600, 900  # Your screen resolution
x = (screen_w - w_w) // 2
y = (screen_h - w_h) // 2

# Move window to the center
cv2.moveWindow(window_name, x, y)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame")
        break

    cv2.imshow(window_name, frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

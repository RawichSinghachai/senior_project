import cv2

# Open the webcam
cap = cv2.VideoCapture(1)

while True:
    # Read frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally (1 = horizontal, 0 = vertical, -1 = both)
    frame = cv2.flip(frame, 1)

    # Display the flipped frame
    cv2.imshow('Flipped Webcam', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the windows
cap.release()
cv2.destroyAllWindows()

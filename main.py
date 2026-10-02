import cv2

# Load YuNet face detection model
model = "face_detection_yunet_2023mar.onnx"

face_detector = cv2.FaceDetectorYN.create(
    model,
    "",
    (320, 320),
    0.9,   # confidence threshold
    0.3,   # NMS threshold
    5000   # maximum detections
)

# Open webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Could not access the webcam.")
    exit()

while True:
    success, frame = camera.read()

    if not success:
        print("Could not read from webcam.")
        break

    # Get frame dimensions
    height, width = frame.shape[:2]

    # Tell the detector the current image size
    face_detector.setInputSize((width, height))

    # Detect faces
    _, faces = face_detector.detect(frame)

    # Draw results
    if faces is not None:
        for face in faces:
            x, y, w, h = face[:4]

            # Draw rectangle
            cv2.rectangle(
                frame,
                (int(x), int(y)),
                (int(x + w), int(y + h)),
                (255, 0, 0),
                2
            )

            # Display confidence
            confidence = face[-1]

            cv2.putText(
                frame,
                f"Face: {confidence:.2f}",
                (int(x), int(y) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )

    # Show webcam
    cv2.imshow("Face Attendance System", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
camera.release()
cv2.destroyAllWindows()
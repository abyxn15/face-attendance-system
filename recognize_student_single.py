import cv2
import os
from attendance import create_database, mark_attendance
# -----------------------------
# MODEL FILES
# -----------------------------
DETECTOR_MODEL = "face_detection_yunet_2023mar.onnx"
RECOGNITION_MODEL = "face_recognition_sface_2021dec_int8.onnx"

# -----------------------------
# REGISTERED STUDENT
# -----------------------------
STUDENT_USN = "4JK24AD021"
STUDENT_NAME = "Abyan"

FACE_IMAGE = os.path.join("students", STUDENT_USN, "face.jpg")

# -----------------------------
# LOAD MODELS
# -----------------------------
detector = cv2.FaceDetectorYN.create(
    DETECTOR_MODEL,
    "",
    (320, 320)
)

recognizer = cv2.FaceRecognizerSF.create(
    RECOGNITION_MODEL,
    ""
)

# -----------------------------
# LOAD REGISTERED FACE
# -----------------------------
registered_image = cv2.imread(FACE_IMAGE)

if registered_image is None:
    print("ERROR: Could not find registered face:")
    print(FACE_IMAGE)
    exit()

# Set detector input size
detector.setInputSize(
    (registered_image.shape[1], registered_image.shape[0])
)

_, registered_faces = detector.detect(registered_image)

if registered_faces is None or len(registered_faces) == 0:
    print("ERROR: No face found in registered face image.")
    exit()

# Take the first detected face
registered_face = registered_faces[0]

# Align the registered face
aligned_registered = recognizer.alignCrop(
    registered_image,
    registered_face
)

# Extract face feature
registered_feature = recognizer.feature(
    aligned_registered
)

print("Registered face loaded successfully!")

# Create attendance database if it doesn't exist
create_database()
attendance_marked = False
print("Starting camera...")

# -----------------------------
# START WEBCAM
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    exit()

while True:

    ret, frame = cap.read()

    if not ret:
        print("ERROR: Could not read webcam.")
        break

    # Set detector input size to current frame
    detector.setInputSize(
        (frame.shape[1], frame.shape[0])
    )

    # Detect faces
    _, faces = detector.detect(frame)

    if faces is not None:

        for face in faces:

            # Align detected face
            aligned_face = recognizer.alignCrop(
                frame,
                face
            )

            # Extract feature
            live_feature = recognizer.feature(
                aligned_face
            )

            # Compare with registered face
            score = recognizer.match(
                registered_feature,
                live_feature,
                cv2.FaceRecognizerSF_FR_COSINE
            )

            # Recognition threshold
            if score >= 0.363:

                text = f"Recognized: {STUDENT_NAME}"
                text2 = f"Similarity: {score:.2f}"

    # Mark attendance only once
                if not attendance_marked:
                    marked = mark_attendance(STUDENT_NAME, STUDENT_USN)

                    if marked:
                        print("Attendance marked successfully!")
                    else:
                        print("Attendance was already marked today.")

                    attendance_marked = True

            else:

                text = "Unknown"
                text2 = f"Similarity: {score:.2f}"

            # Face coordinates
            x, y, w, h = face[:4].astype(int)

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                text,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                text2,
                (x, y + h + 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

    cv2.imshow(
        "Face Recognition",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# -----------------------------
# CLEANUP
# -----------------------------
cap.release()
cv2.destroyAllWindows()

print("Face recognition stopped.")
import cv2
import os

# ==============================
# Load face detection model
# ==============================

MODEL = "face_detection_yunet_2023mar.onnx"

face_detector = cv2.FaceDetectorYN.create(
    MODEL,
    "",
    (320, 320),
    0.9,
    0.3,
    5000
)


# ==============================
# Get student information
# ==============================

print("\n==============================")
print("   STUDENT REGISTRATION")
print("==============================\n")

name = input("Enter student name: ")
usn = input("Enter USN: ")
semester = input("Enter semester: ")
section = input("Enter section: ")


# ==============================
# Create student folder
# ==============================

student_folder = os.path.join("students", usn)

os.makedirs(student_folder, exist_ok=True)


# ==============================
# Open webcam
# ==============================

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Could not access webcam.")
    exit()


print("\nCamera started.")
print("Look at the camera.")
print("Press SPACE to capture your face.")
print("Press Q to cancel.\n")


while True:

    success, frame = camera.read()

    if not success:
        print("Could not read webcam.")
        break

    height, width = frame.shape[:2]

    face_detector.setInputSize((width, height))

    _, faces = face_detector.detect(frame)

    # Draw face detection boxes
    if faces is not None:

        for face in faces:

            x, y, w, h = face[:4]

            cv2.rectangle(
                frame,
                (int(x), int(y)),
                (int(x + w), int(y + h)),
                (255, 0, 0),
                2
            )

    cv2.putText(
        frame,
        "SPACE = Capture | Q = Quit",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.imshow("Student Registration", frame)

    key = cv2.waitKey(1) & 0xFF

    # Capture face
    if key == 32:  # SPACE

        if faces is None or len(faces) == 0:

            print("No face detected. Try again.")

        elif len(faces) > 1:

            print("Multiple faces detected.")
            print("Please make sure only one person is in front of the camera.")

        else:

            face = faces[0]

            x, y, w, h = face[:4]

            x = int(x)
            y = int(y)
            w = int(w)
            h = int(h)

            # Add a small margin around face
            margin = 20

            x1 = max(0, x - margin)
            y1 = max(0, y - margin)
            x2 = min(width, x + w + margin)
            y2 = min(height, y + h + margin)

            face_image = frame[y1:y2, x1:x2]

            # Save face image
            image_path = os.path.join(
                student_folder,
                "face.jpg"
            )

            cv2.imwrite(image_path, face_image)

            # Save student information
            info_path = os.path.join(
                student_folder,
                "student.txt"
            )

            with open(info_path, "w") as file:

                file.write(f"Name: {name}\n")
                file.write(f"USN: {usn}\n")
                file.write(f"Semester: {semester}\n")
                file.write(f"Section: {section}\n")

            print("\nStudent registered successfully!")
            print(f"Name: {name}")
            print(f"USN: {usn}")
            print(f"Face saved to: {image_path}")

            break

    # Quit
    elif key == ord("q"):

        print("Registration cancelled.")
        break


camera.release()
cv2.destroyAllWindows()
import cv2
import os
import time


# ---------------------------------
# MODEL
# ---------------------------------

DETECTOR_MODEL = "face_detection_yunet_2023mar.onnx"

detector = cv2.FaceDetectorYN.create(
    DETECTOR_MODEL,
    "",
    (320, 320)
)


# ---------------------------------
# STUDENT DETAILS
# ---------------------------------

name = input("Enter student name: ").strip()
usn = input("Enter USN: ").strip()
semester = input("Enter semester: ").strip()
section = input("Enter section: ").strip()


# ---------------------------------
# CREATE STUDENT FOLDER
# ---------------------------------

student_folder = os.path.join(
    "students",
    usn
)

os.makedirs(
    student_folder,
    exist_ok=True
)


# ---------------------------------
# SAVE STUDENT INFORMATION
# ---------------------------------

student_file = os.path.join(
    student_folder,
    "student.txt"
)

with open(
    student_file,
    "w",
    encoding="utf-8"
) as file:

    file.write(f"Name: {name}\n")
    file.write(f"USN: {usn}\n")
    file.write(f"Semester: {semester}\n")
    file.write(f"Section: {section}\n")


# ---------------------------------
# CAMERA
# ---------------------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("ERROR: Could not open webcam.")
    exit()


print("\nRegistration started.")
print("Look at the camera.")
print("Move your face slightly between captures.")
print("Press SPACE to capture.")
print("Press Q to cancel.\n")


# ---------------------------------
# CAPTURE SETTINGS
# ---------------------------------

total_samples = 5
captured_samples = 0

last_capture_time = 0
capture_delay = 1.0


# ---------------------------------
# MAIN LOOP
# ---------------------------------

while captured_samples < total_samples:

    ret, frame = cap.read()

    if not ret:
        print("Could not read webcam.")
        break


    detector.setInputSize(
        (frame.shape[1], frame.shape[0])
    )


    _, faces = detector.detect(frame)


    # ---------------------------------
    # DRAW FACE
    # ---------------------------------

    if faces is not None:

        for face in faces:

            x, y, w, h = face[:4].astype(int)

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )


    # ---------------------------------
    # DISPLAY INSTRUCTIONS
    # ---------------------------------

    message = (
        f"Samples: {captured_samples}/{total_samples} "
        f"| SPACE = Capture | Q = Quit"
    )

    cv2.putText(
        frame,
        message,
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    cv2.imshow(
        "Student Registration",
        frame
    )


    key = cv2.waitKey(1) & 0xFF


    # ---------------------------------
    # CAPTURE
    # ---------------------------------

    if key == ord(" "):

        current_time = time.time()

        if current_time - last_capture_time < capture_delay:
            continue


        if faces is None or len(faces) == 0:

            print("No face detected. Try again.")
            continue


        # Use the largest detected face
        face = max(
            faces,
            key=lambda f: f[2] * f[3]
        )


        x, y, w, h = face[:4].astype(int)


        # Add margin around face
        margin = int(0.25 * max(w, h))

        x1 = max(0, x - margin)
        y1 = max(0, y - margin)

        x2 = min(
            frame.shape[1],
            x + w + margin
        )

        y2 = min(
            frame.shape[0],
            y + h + margin
        )


        face_crop = frame[
            y1:y2,
            x1:x2
        ]


        if face_crop.size == 0:
            continue


        captured_samples += 1


        filename = os.path.join(
            student_folder,
            f"face_{captured_samples}.jpg"
        )


        cv2.imwrite(
            filename,
            face_crop
        )


        print(
            f"Captured sample "
            f"{captured_samples}/{total_samples}"
        )


        last_capture_time = current_time


    # ---------------------------------
    # QUIT
    # ---------------------------------

    elif key == ord("q"):

        print("Registration cancelled.")
        break


# ---------------------------------
# CLEANUP
# ---------------------------------

cap.release()
cv2.destroyAllWindows()


# ---------------------------------
# RESULT
# ---------------------------------

if captured_samples == total_samples:

    print("\nRegistration completed successfully!")

    print(
        f"Saved {total_samples} face samples for {name}."
    )

else:

    print("\nRegistration incomplete.")
import cv2
import os

from attendance import create_database, mark_attendance


# ---------------------------------
# MODEL FILES
# ---------------------------------

DETECTOR_MODEL = "face_detection_yunet_2023mar.onnx"
RECOGNITION_MODEL = "face_recognition_sface_2021dec_int8.onnx"

STUDENTS_FOLDER = "students"

# Recognition threshold
THRESHOLD = 0.363


# ---------------------------------
# LOAD MODELS
# ---------------------------------

detector = cv2.FaceDetectorYN.create(
    DETECTOR_MODEL,
    "",
    (320, 320)
)

recognizer = cv2.FaceRecognizerSF.create(
    RECOGNITION_MODEL,
    ""
)


# ---------------------------------
# LOAD REGISTERED STUDENTS
# ---------------------------------

registered_students = []


for usn in os.listdir(STUDENTS_FOLDER):

    student_folder = os.path.join(
        STUDENTS_FOLDER,
        usn
    )

    if not os.path.isdir(student_folder):
        continue


    student_file = os.path.join(
        student_folder,
        "student.txt"
    )

    if not os.path.isfile(student_file):
        continue


    # ---------------------------------
    # READ STUDENT INFORMATION
    # ---------------------------------

    with open(student_file, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()


    name = usn

    for line in lines:

        if line.startswith("Name:"):
            name = line.split(":", 1)[1].strip()


    # ---------------------------------
    # FIND FACE IMAGES
    # ---------------------------------

    face_images = []


    # New multi-sample format
    for filename in sorted(os.listdir(student_folder)):

        if (
            filename.startswith("face_")
            and filename.endswith(".jpg")
        ):

            face_images.append(
                os.path.join(
                    student_folder,
                    filename
                )
            )


    # Old single-sample format
    if len(face_images) == 0:

        old_face = os.path.join(
            student_folder,
            "face.jpg"
        )

        if os.path.isfile(old_face):

            face_images.append(old_face)


    if len(face_images) == 0:

        print(
            f"No face images found for {name} ({usn})"
        )

        continue


    # ---------------------------------
    # GENERATE FEATURES
    # ---------------------------------

    student_features = []


    for face_image_path in face_images:

        image = cv2.imread(face_image_path)

        if image is None:
            print(
                f"Could not read: {face_image_path}"
            )
            continue


        # Detect face
        detector.setInputSize(
            (image.shape[1], image.shape[0])
        )

        _, faces = detector.detect(image)


        if faces is None or len(faces) == 0:

            print(
                f"Could not detect face in "
                f"{face_image_path}"
            )

            continue


        # Use first detected face
        face = faces[0]


        # Align face
        aligned_face = recognizer.alignCrop(
            image,
            face
        )


        # Generate feature
        feature = recognizer.feature(
            aligned_face
        )


        student_features.append(feature)


    # ---------------------------------
    # SAVE STUDENT
    # ---------------------------------

    if len(student_features) == 0:

        print(
            f"No usable face samples for "
            f"{name} ({usn})"
        )

        continue


    registered_students.append({
        "name": name,
        "usn": usn,
        "features": student_features
    })


    print(
        f"Loaded student: {name} ({usn}) "
        f"- {len(student_features)} sample(s)"
    )


# ---------------------------------
# CHECK STUDENTS
# ---------------------------------

if len(registered_students) == 0:

    print("No registered students found.")

    exit()


print(
    f"\nTotal registered students: "
    f"{len(registered_students)}"
)


# ---------------------------------
# DATABASE
# ---------------------------------

create_database()


# ---------------------------------
# CAMERA
# ---------------------------------

cap = cv2.VideoCapture(0)


if not cap.isOpened():

    print("ERROR: Could not open webcam.")

    exit()


print("\nStarting attendance system...")
print("Press Q to quit.")


# ---------------------------------
# ATTENDANCE FLAG
# ---------------------------------

attendance_done = set()


# ---------------------------------
# MAIN LOOP
# ---------------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        break


    detector.setInputSize(
        (frame.shape[1], frame.shape[0])
    )


    _, faces = detector.detect(frame)


    if faces is not None:

        for face in faces:

            # ---------------------------------
            # ALIGN LIVE FACE
            # ---------------------------------

            aligned_face = recognizer.alignCrop(
                frame,
                face
            )


            # ---------------------------------
            # LIVE FEATURE
            # ---------------------------------

            live_feature = recognizer.feature(
                aligned_face
            )


            # ---------------------------------
            # FIND BEST MATCH
            # ---------------------------------

            best_score = -1
            best_student = None


            for student in registered_students:

                student_best_score = -1


                # Compare against every sample
                for stored_feature in student["features"]:

                    score = recognizer.match(
                        stored_feature,
                        live_feature,
                        cv2.FaceRecognizerSF_FR_COSINE
                    )


                    if score > student_best_score:

                        student_best_score = score


                # Compare student's best score
                # against the overall best
                if student_best_score > best_score:

                    best_score = student_best_score
                    best_student = student


            # ---------------------------------
            # FACE POSITION
            # ---------------------------------

            x, y, w, h = face[:4].astype(int)


            # ---------------------------------
            # RECOGNITION
            # ---------------------------------

            if best_score >= THRESHOLD:

                name = best_student["name"]
                usn = best_student["usn"]


                # ---------------------------------
                # MARK ATTENDANCE
                # ---------------------------------

                if usn not in attendance_done:

                    marked = mark_attendance(
                        name,
                        usn
                    )

                    attendance_done.add(usn)


                    if marked:

                        print(
                            f"Attendance marked: "
                            f"{name} ({usn})"
                        )


                text = name
                text2 = (
                    f"{usn} | "
                    f"{best_score:.2f}"
                )


            else:

                text = "Unknown"

                text2 = (
                    f"Similarity: "
                    f"{best_score:.2f}"
                )


            # ---------------------------------
            # DRAW FACE
            # ---------------------------------

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


    # ---------------------------------
    # DISPLAY
    # ---------------------------------

    cv2.imshow(
        "Face Attendance System",
        frame
    )


    # ---------------------------------
    # QUIT
    # ---------------------------------

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ---------------------------------
# CLEANUP
# ---------------------------------

cap.release()

cv2.destroyAllWindows()

print("\nAttendance system stopped.")
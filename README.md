# Face Recognition Based Automated Student Attendance Management System

An automated student attendance system using face detection and face recognition.

## Features

- Student registration with face samples
- Real-time face detection
- Face recognition using registered students
- Automatic attendance marking
- Duplicate attendance prevention
- SQLite attendance database
- Attendance viewing dashboard
- CSV attendance report export
- Multi-student recognition
- Multiple face samples for improved recognition

## Technologies Used

- Python
- OpenCV
- YuNet Face Detector
- SFace Face Recognition
- SQLite
- Tkinter
- Pandas

## Project Structure

```text
face-attendance-system/
│
├── app.py
├── register_student.py
├── register_student_multi.py
├── recognize_student.py
├── recognize_all.py
├── attendance.py
├── view_attendance.py
│
├── face_detection_yunet_2023mar.onnx
├── face_recognition_sface_2021dec_int8.onnx
│
├── students/
│   └── student_USN/
│       ├── face_1.jpg
│       ├── face_2.jpg
│       ├── face_3.jpg
│       ├── face_4.jpg
│       ├── face_5.jpg
│       └── student.txt
│
├── attendance.db
└── attendance_report.csv
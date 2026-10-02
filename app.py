import tkinter as tk
from tkinter import messagebox
import subprocess
import sys


def run_program(filename):
    try:
        subprocess.Popen([sys.executable, filename])
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Could not start {filename}\n\n{e}"
        )


def register_student():
    run_program("register_student_multi.py")


def start_attendance():
    run_program("recognize_all.py")


def view_attendance():
    run_program("view_attendance.py")


def exit_app():
    root.destroy()


# -----------------------------
# MAIN WINDOW
# -----------------------------

root = tk.Tk()

root.title("Face Attendance System")
root.geometry("600x500")
root.resizable(False, False)


# -----------------------------
# TITLE
# -----------------------------

title = tk.Label(
    root,
    text="Face Attendance System",
    font=("Arial", 26, "bold")
)

title.pack(pady=(50, 10))


subtitle = tk.Label(
    root,
    text="Automated Student Attendance Using Face Recognition",
    font=("Arial", 11)
)

subtitle.pack(pady=(0, 35))


# -----------------------------
# BUTTONS
# -----------------------------

register_button = tk.Button(
    root,
    text="Register Student",
    font=("Arial", 14),
    width=25,
    height=2,
    command=register_student
)

register_button.pack(pady=10)


attendance_button = tk.Button(
    root,
    text="Start Attendance",
    font=("Arial", 14),
    width=25,
    height=2,
    command=start_attendance
)

attendance_button.pack(pady=10)


view_button = tk.Button(
    root,
    text="View Attendance",
    font=("Arial", 14),
    width=25,
    height=2,
    command=view_attendance
)

view_button.pack(pady=10)


exit_button = tk.Button(
    root,
    text="Exit",
    font=("Arial", 14),
    width=25,
    height=2,
    command=exit_app
)

exit_button.pack(pady=10)


# -----------------------------
# FOOTER
# -----------------------------

footer = tk.Label(
    root,
    text="AI & Data Science Project",
    font=("Arial", 9)
)

footer.pack(side=tk.BOTTOM, pady=20)


# -----------------------------
# START APPLICATION
# -----------------------------

root.mainloop()
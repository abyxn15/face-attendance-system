import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DATABASE = "attendance.db"


def load_attendance():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, usn, date, time
        FROM attendance
        ORDER BY date DESC, time DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records


def refresh_table():
    # Remove existing rows
    for row in table.get_children():
        table.delete(row)

    records = load_attendance()

    for record in records:
        table.insert("", tk.END, values=record)


def export_csv():
    import csv

    records = load_attendance()

    if not records:
        messagebox.showinfo("Export", "No attendance records found.")
        return

    filename = "attendance_report.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Name",
            "USN",
            "Date",
            "Time"
        ])

        writer.writerows(records)

    messagebox.showinfo(
        "Export Successful",
        f"Attendance report saved as:\n{filename}"
    )


# -----------------------------
# WINDOW
# -----------------------------

root = tk.Tk()

root.title("Face Attendance System")
root.geometry("800x500")

title = tk.Label(
    root,
    text="Face Recognition Attendance",
    font=("Arial", 20, "bold")
)

title.pack(pady=20)


# -----------------------------
# TABLE
# -----------------------------

columns = (
    "Name",
    "USN",
    "Date",
    "Time"
)

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

for column in columns:

    table.heading(
        column,
        text=column
    )

    table.column(
        column,
        width=170
    )

table.pack(
    fill=tk.BOTH,
    expand=True,
    padx=20,
    pady=10
)


# -----------------------------
# BUTTONS
# -----------------------------

button_frame = tk.Frame(root)

button_frame.pack(pady=15)


refresh_button = tk.Button(
    button_frame,
    text="Refresh",
    command=refresh_table,
    width=15
)

refresh_button.pack(
    side=tk.LEFT,
    padx=10
)


export_button = tk.Button(
    button_frame,
    text="Export CSV",
    command=export_csv,
    width=15
)

export_button.pack(
    side=tk.LEFT,
    padx=10
)


# Load data when opening
refresh_table()


root.mainloop()
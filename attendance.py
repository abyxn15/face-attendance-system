import sqlite3
from datetime import datetime

# Database file
DATABASE = "attendance.db"


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            usn TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            UNIQUE(usn, date)
        )
    """)

    connection.commit()
    connection.close()


def mark_attendance(name, usn):
    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO attendance (name, usn, date, time)
            VALUES (?, ?, ?, ?)
        """, (name, usn, date, time))

        connection.commit()

        print(f"Attendance marked: {name} - {date} {time}")
        result = True

    except sqlite3.IntegrityError:
        print(f"Attendance already marked today for {name}")
        result = False

    connection.close()

    return result


def show_attendance():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, usn, date, time
        FROM attendance
        ORDER BY date DESC, time DESC
    """)

    records = cursor.fetchall()

    connection.close()

    print("\n----- ATTENDANCE RECORDS -----")

    if not records:
        print("No attendance records found.")
    else:
        for record in records:
            print(
                f"Name: {record[0]} | "
                f"USN: {record[1]} | "
                f"Date: {record[2]} | "
                f"Time: {record[3]}"
            )


if __name__ == "__main__":

    create_database()

    print("Attendance database created successfully.")

    # Test attendance
    mark_attendance("Abyan", "4JK24AD021")

    show_attendance()
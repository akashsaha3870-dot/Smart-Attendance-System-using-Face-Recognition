import mysql.connector

# -----------------------------
# MySQL Connection
# -----------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="akash@2006",   # change if needed
    database="smart_attendance"
)

cursor = db.cursor()

print("\n===== Attendance Summary Report =====\n")

# -----------------------------------
# Get total working days
# -----------------------------------
cursor.execute("""
SELECT COUNT(DISTINCT date) 
FROM attendance_log;
""")

total_days = cursor.fetchone()[0]

if total_days == 0:
    print("No attendance records found.")
    exit()

# -----------------------------------
# Get attendance per student
# -----------------------------------
query = """
SELECT s.name,
       COUNT(a.log_id) AS present_days
FROM students s
LEFT JOIN attendance_log a
ON s.id = a.student_id
GROUP BY s.name
ORDER BY s.name;
"""

cursor.execute(query)
results = cursor.fetchall()

# -----------------------------------
# Print Report
# -----------------------------------
for name, present_days in results:
    percentage = (present_days / total_days) * 100
    print(f"{name}")
    print(f"   Days Present : {present_days}")
    print(f"   Attendance % : {percentage:.2f}%")
    print("-----------------------------------")

print(f"\nTotal Working Days: {total_days}")

cursor.close()
db.close()
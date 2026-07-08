import cv2
from deepface import DeepFace
import numpy as np
import os
import mysql.connector
from datetime import datetime

# ------------------------------------------
# MySQL Connection
# ------------------------------------------

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="akash@2006",   # change if needed
    database="smart_attendance"
)

cursor = db.cursor(buffered=True)

print("Connected to MySQL")

# ------------------------------------------
# Load Reference Embeddings
# ------------------------------------------

dataset_path = "dataset"

known_embeddings = []
known_names = []

print("Loading known faces...")

for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)

    if os.path.isdir(person_folder):

        embeddings = []

        for img_name in os.listdir(person_folder):
            img_path = os.path.join(person_folder, img_name)

            try:
                embedding = DeepFace.represent(
                    img_path=img_path,
                    model_name="Facenet",
                    enforce_detection=False
                )[0]["embedding"]

                embeddings.append(embedding)

            except:
                pass

        if len(embeddings) > 0:
            avg_embedding = np.mean(embeddings, axis=0)
            known_embeddings.append(avg_embedding)
            known_names.append(person_name)

print("Faces loaded:", known_names)

# ------------------------------------------
# Webcam Start
# ------------------------------------------

cap = cv2.VideoCapture(0)

frame_count = 0
name = "Unknown"
max_similarity = 0
last_marked = None

print("Webcam started... Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Run recognition every 5 frames (performance optimization)
    if frame_count % 5 == 0:
        try:
            embedding = DeepFace.represent(
                img_path=frame,
                model_name="Facenet",
                enforce_detection=False
            )[0]["embedding"]

            max_similarity = -1
            identity = "Unknown"

            for i, known_embedding in enumerate(known_embeddings):

                cosine_similarity = np.dot(known_embedding, embedding) / (
                    np.linalg.norm(known_embedding) * np.linalg.norm(embedding)
                )

                if cosine_similarity > max_similarity:
                    max_similarity = cosine_similarity
                    identity = known_names[i]

            # Threshold
            if max_similarity > 0.55:
                name = identity
            else:
                name = "Unknown"

        except:
            name = "Unknown"

    # ------------------------------------------
    # Mark Attendance (Only Once Per Day)
    # ------------------------------------------

    if name != "Unknown" and name != last_marked:

        today = datetime.now().date()

        cursor.execute("SELECT id FROM students WHERE name=%s", (name,))
        student = cursor.fetchone()

        if student:
            student_id = student[0]

            cursor.execute(
                "SELECT * FROM attendance_log WHERE student_id=%s AND date=%s",
                (student_id, today)
            )

            result = cursor.fetchone()

            if result is None:
                now = datetime.now()
                cursor.execute(
                    "INSERT INTO attendance_log (student_id, date, time) VALUES (%s, %s, %s)",
                    (student_id, now.date(), now.time())
                )
                db.commit()
                print(f"{name} attendance marked.")
            else:
                print(f"{name} already marked today.")

        last_marked = name

    # ------------------------------------------
    # Draw Face Box + UI
    # ------------------------------------------

    try:
        faces = DeepFace.extract_faces(frame, enforce_detection=False)

        for face in faces:
            x = face["facial_area"]["x"]
            y = face["facial_area"]["y"]
            w = face["facial_area"]["w"]
            h = face["facial_area"]["h"]

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            confidence_text = f"{name} ({round(max_similarity, 2)})"

            cv2.putText(frame,
                        confidence_text,
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2)

    except:
        pass

    # Header
    cv2.putText(frame,
                "AI Smart Attendance System",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2)

    # Footer
    cv2.putText(frame,
                "Press Q to Exit",
                (20, 470),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (200, 200, 200),
                1)

    cv2.imshow("AI Smart Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
db.close()
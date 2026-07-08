import cv2
from deepface import DeepFace
import numpy as np

print("Loading AI Face Recognition Model...")

# ----------------------------------------
# Step 1: Load and average reference embeddings
# ----------------------------------------

reference_embeddings = []

reference_images = [
    "dataset/Akash/Akash1.jpg",
    "dataset/Akash/Akash2.jpg"
]

for img_path in reference_images:
    embedding = DeepFace.represent(
        img_path=img_path,
        model_name="Facenet",
        enforce_detection=False
    )[0]["embedding"]
    
    reference_embeddings.append(embedding)

# Average embedding (more stable recognition)
reference_embedding = np.mean(reference_embeddings, axis=0)

print("Reference embeddings loaded successfully.")

# ----------------------------------------
# Step 2: Start Webcam
# ----------------------------------------

cap = cv2.VideoCapture(0)

frame_count = 0
name = "Unknown"

print("Webcam started... Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Process every 5th frame for smoothness
    if frame_count % 5 == 0:
        try:
            embedding = DeepFace.represent(
                img_path=frame,
                model_name="Facenet",
                enforce_detection=False
            )[0]["embedding"]

            # Cosine similarity
            cosine_similarity = np.dot(reference_embedding, embedding) / (
                np.linalg.norm(reference_embedding) * np.linalg.norm(embedding)
            )

            print("Similarity:", round(cosine_similarity, 3))  # Debug

            # Threshold tuning (adjust if needed)
            if cosine_similarity > 0.55:
                name = "Akash"
            else:
                name = "Unknown"

        except:
            name = "Unknown"

    # Display result
    cv2.putText(frame, name, (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2)

    cv2.imshow("AI Smart Attendance - Akash", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
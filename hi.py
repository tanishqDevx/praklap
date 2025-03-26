import face_recognition
import cv2
import numpy as np
import os

# Paths for storing encoded faces
encoding_file = "face_encodings.npy"
names_file = "face_names.npy"
people_images_folder = "/home/tanishq/Desktop/my_images"

# Variables to hold encodings
known_face_encodings = []
known_face_names = []

def save_encodings():
    """Saves face encodings and names."""
    np.save(encoding_file, np.array(known_face_encodings, dtype=object))
    np.save(names_file, np.array(known_face_names, dtype=object))
    print("💾 Encodings saved!")

def load_encodings():
    """Loads encodings if the file exists."""
    global known_face_encodings, known_face_names
    if os.path.exists(encoding_file) and os.path.exists(names_file):
        known_face_encodings = np.load(encoding_file, allow_pickle=True).tolist()
        known_face_names = np.load(names_file, allow_pickle=True).tolist()
        return True
    return False

# Load from file if available
if load_encodings():
    print(f"✅ Loaded {len(known_face_encodings)} known faces from cache.")
else:
    print("🔍 Loading known faces...")
    for person_name in os.listdir(people_images_folder):
        person_folder = os.path.join(people_images_folder, person_name)
        if os.path.isdir(person_folder):
            for filename in os.listdir(person_folder):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(person_folder, filename)
                    image = face_recognition.load_image_file(img_path)

                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        known_face_encodings.append(encodings[0])
                        known_face_names.append(person_name)
                        print(f"✅ Loaded: {filename} for {person_name}")
                    else:
                        print(f"❌ Warning: No face found in {filename}, skipping...")

    if known_face_encodings:
        save_encodings()
    else:
        raise ValueError("❌ No faces found. Ensure images contain clear faces.")

print(f"🎉 Ready! Found {len(known_face_encodings)} known face(s).")

# Start webcam
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    raise RuntimeError("❌ Could not access the webcam. Ensure it is connected and accessible.")

print("📷 Webcam started. Press 'q' to exit.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("❌ Failed to grab frame. Exiting...")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame, model="hog")
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)
        name = "Unknown Person"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index] and face_distances[best_match_index] < 0.4:
            name = known_face_names[best_match_index]

        print(f"Detected: {name} (Distance: {face_distances[best_match_index]:.2f})")

        color = (0, 255, 0) if name != "Unknown Person" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, bottom + 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, color, 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

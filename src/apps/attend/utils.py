import face_recognition
import numpy as np

def encode_face(image_file):
    img = face_recognition.load_image_file(image_file)
    encoding = face_recognition.face_encodings(img)
    if encoding:
        return encoding[0].tobytes()
    return None

def match_face (image_file, student):
    img = face_recognition.load_image_file(image_file)
    encodings = face_recognition.face_encodings(img)
    if not encodings:
        return False
    student_encoding = np.frombuffer(student.face_encoding, dtype=np.float64)
    results = face_recognition.compare_faces([student_encoding], encodings[0])
    return results[0]
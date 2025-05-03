import cv2
import numpy as np
import webbrowser
from datetime import datetime
import os
import face_recognition
import time

def compare_faces(face1_encoding, face2_encoding, tolerance=0.6):
    # Use face_recognition.compare_faces with a tolerance value to allow for minor variations in face encodings
    return face_recognition.compare_faces([face1_encoding], face2_encoding, tolerance=tolerance)[0]

def main():
    # Load the reference image and encode its face
    reference_img = face_recognition.load_image_file('aryan.jpg')
    reference_encoding = face_recognition.face_encodings(reference_img)[0]  # Reference face encoding
    
    if reference_encoding is None:
        print("Error: Could not find a face in the reference image")
        return

    # Initialize face cascade classifier and video capture
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    last_face_detected_time = time.time()  # Track time when face was last detected
    qr_generated = False  # Flag to track QR generation
    previous_qr_timestamp = None  # Store the timestamp of the previous QR code to delete it
    qr_image_path = "qr_code.png"  # Path to the QR code image
    recent_qr_image = None  # Store the most recent QR image

    qr_refresh_interval = 30  # Interval in seconds to refresh the QR code
    last_qr_time = time.time()  # Track the time when the last QR was generated

    last_match_time = 0  # Track the time when the last face match was found

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            last_face_detected_time = time.time()  # Reset face detection timer

        # Iterate over all detected faces
        for (x, y, w, h) in faces:
            # Draw rectangle around detected face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Extract the face ROI (Region Of Interest)
            face_roi = frame[y:y + h, x:x + w]

            # Use face_recognition to detect face encodings
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            if len(face_encodings) > 0:
                face_encoding = face_encodings[0]
                
                # Compare with reference encoding using a threshold for tolerance
                if compare_faces(face_encoding, reference_encoding, tolerance=0.6):
                    # Check if 5 seconds have passed since the last match
                    current_time = time.time()
                    if current_time - last_match_time > 5:
                        cv2.putText(frame, "Match Found!", (x, y - 10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        # Open Instagram URL if match is found
                        if os.path.exists('l.html'):
                            webbrowser.open('l.html')
                        
                        # Update the last match time
                        last_match_time = current_time

                else:
                    cv2.putText(frame, "No Match", (x, y - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            else:
                cv2.putText(frame, "No Face Found", (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Display the video frame
        cv2.imshow('Face Recognition', frame)

        # Break loop on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

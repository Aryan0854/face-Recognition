## Face Recognition Access System

This project uses face recognition to grant access by verifying a live face against a reference image. If the face matches, it opens an HTML page indicating access is granted.

### 📁 Files Included

* `face_match.py`: Python script that captures live video, detects faces, compares them to a reference image, and opens a webpage on a successful match.
* `l.html`: Webpage shown when access is granted.
* `aryan.jpg`: Reference image used for face comparison (you need to place this in the same directory).

### 🛠 Requirements

* Python 3.x
* OpenCV (`cv2`)
* `face_recognition`
* NumPy

Install dependencies using:

```bash
pip install opencv-python face_recognition numpy
```

### ▶️ How to Run

1. Place your reference image as `aryan.jpg` in the same directory.
2. Make sure `l.html` exists in the same directory.
3. Run the script:

```bash
python face_match.py
```

4. Allow webcam access. When a matching face is detected, the browser will open `l.html` displaying **Access Granted**.

### 📝 Notes

* The system uses a 5-second delay between consecutive successful matches.
* Adjust the `tolerance` value in `compare_faces()` to make matching stricter or more lenient.

### 🔒 Security

This is a demo and should not be used in high-security systems without additional safeguards (e.g., liveness detection).

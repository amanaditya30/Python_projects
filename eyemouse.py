import cv2
import dlib
import pyautogui
import numpy as np
from scipy.spatial import distance

# Load Dlib's face detector and shape predictor (download shape_predictor_68_face_landmarks.dat)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Indices for eye landmarks
LEFT_EYE = list(range(36, 42))
RIGHT_EYE = list(range(42, 48))

# Screen size
screen_width, screen_height = pyautogui.size()
cam_width, cam_height = 640, 480

def eye_aspect_ratio(eye_points):
    """Calculate Eye Aspect Ratio (EAR) to detect blinks."""
    A = distance.euclidean(eye_points[1], eye_points[5])
    B = distance.euclidean(eye_points[2], eye_points[4])
    C = distance.euclidean(eye_points[0], eye_points[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Blink detection threshold
BLINK_THRESHOLD = 0.2  
BLINK_FRAMES = 3  # Minimum consecutive frames for a valid blink
blink_counter = 0

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip horizontally for better control
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)
        landmarks_points = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(68)])

        left_eye = landmarks_points[LEFT_EYE]
        right_eye = landmarks_points[RIGHT_EYE]

        # Compute center of eyes
        left_eye_center = np.mean(left_eye, axis=0).astype(int)
        right_eye_center = np.mean(right_eye, axis=0).astype(int)
        eye_center = ((left_eye_center[0] + right_eye_center[0]) // 2, (left_eye_center[1] + right_eye_center[1]) // 2)

        # Map eye position to screen coordinates
        screen_x = np.interp(eye_center[0], [0, cam_width], [0, screen_width])
        screen_y = np.interp(eye_center[1], [0, cam_height], [0, screen_height])
        pyautogui.moveTo(screen_x, screen_y)

        # Blink detection
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0

        if ear < BLINK_THRESHOLD:
            blink_counter += 1
        else:
            if blink_counter >= BLINK_FRAMES:
                pyautogui.click()  # Simulate click
            blink_counter = 0

        # Draw eye landmarks
        for point in left_eye:
            cv2.circle(frame, tuple(point), 2, (0, 255, 0), -1)
        for point in right_eye:
            cv2.circle(frame, tuple(point), 2, (0, 255, 0), -1)

    cv2.imshow("Eye Cursor Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()

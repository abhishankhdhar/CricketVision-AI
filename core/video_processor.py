import os
import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose

def save_uploaded_video(uploaded_file, directory):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

def analyze_video(video_path, max_frames=300):
    """
    Extract MediaPipe pose landmarks from sampled video frames.
    Returns a list of per-frame landmark dictionaries.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open the uploaded video.")

    results_data = []
    frame_count = 0

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as pose:

        while cap.isOpened() and frame_count < max_frames:
            ok, frame = cap.read()
            if not ok:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = pose.process(rgb)

            if result.pose_landmarks:
                frame_landmarks = []
                for lm in result.pose_landmarks.landmark:
                    frame_landmarks.append({
                        "x": float(lm.x),
                        "y": float(lm.y),
                        "z": float(lm.z),
                        "visibility": float(lm.visibility),
                    })
                results_data.append(frame_landmarks)

            frame_count += 1

    cap.release()

    if not results_data:
        raise ValueError(
            "No person pose was detected. Use a clear full-body batting video."
        )

    return results_data

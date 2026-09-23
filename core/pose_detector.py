import mediapipe as mp

mp_pose = mp.solutions.pose

class PoseDetector:
    """Reusable MediaPipe pose detector wrapper."""

    def __init__(self):
        self.pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def close(self):
        self.pose.close()

import statistics
from core.angle_calculator import calculate_angle

# MediaPipe Pose landmark indexes:
# 11 left shoulder, 12 right shoulder
# 13 left elbow, 14 right elbow
# 15 left wrist, 16 right wrist
# 23 left hip, 24 right hip
# 25 left knee, 26 right knee
# 27 left ankle, 28 right ankle

def _angle(frame, a, b, c):
    return calculate_angle(frame[a], frame[b], frame[c])

def _avg(values, default=0.0):
    return statistics.mean(values) if values else default

def analyze_technique(frames):
    left_knee = []
    right_knee = []
    left_elbow = []
    right_elbow = []
    shoulder_tilt = []
    head_movement = []

    for frame in frames:
        try:
            left_knee.append(_angle(frame, 23, 25, 27))
            right_knee.append(_angle(frame, 24, 26, 28))
            left_elbow.append(_angle(frame, 11, 13, 15))
            right_elbow.append(_angle(frame, 12, 14, 16))

            # Approximate shoulder tilt from shoulder y difference.
            shoulder_tilt.append(abs(frame[11]["y"] - frame[12]["y"]))

            # Head proxy: average shoulder position is compared with wrist/head proxy.
            head_movement.append(frame[0]["y"])
        except (IndexError, KeyError):
            continue

    return {
        "left_knee_angle": round(_avg(left_knee), 2),
        "right_knee_angle": round(_avg(right_knee), 2),
        "left_elbow_angle": round(_avg(left_elbow), 2),
        "right_elbow_angle": round(_avg(right_elbow), 2),
        "shoulder_tilt_average": round(_avg(shoulder_tilt), 4),
        "head_vertical_movement": round(
            (max(head_movement) - min(head_movement)) if head_movement else 0.0, 4
        ),
    }

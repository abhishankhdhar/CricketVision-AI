import math
import statistics


# MediaPipe Pose landmark indexes
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12

LEFT_WRIST = 15
RIGHT_WRIST = 16

LEFT_HIP = 23
RIGHT_HIP = 24


def _distance(p1, p2):
    """Calculate 2D distance between two landmarks."""
    return math.sqrt(
        (p1["x"] - p2["x"]) ** 2
        + (p1["y"] - p2["y"]) ** 2
    )


def _midpoint(p1, p2):
    """Calculate midpoint between two landmarks."""
    return {
        "x": (p1["x"] + p2["x"]) / 2,
        "y": (p1["y"] + p2["y"]) / 2,
    }


def _safe_landmark(frame, index):
    """Return a landmark only when visibility is sufficient."""
    if index >= len(frame):
        return None

    landmark = frame[index]

    if landmark.get("visibility", 0.0) < 0.35:
        return None

    return landmark


def validate_batting_video(frames):
    """
    Validate whether a video contains a batting-like movement.

    This is a pose-based heuristic validator.
    It is NOT a trained machine-learning classifier.
    """

    if not frames:
        return {
            "is_batting": False,
            "confidence": 0.0,
            "reason": "No pose frames were detected.",
        }

    required_landmarks = [
        LEFT_SHOULDER,
        RIGHT_SHOULDER,
        LEFT_WRIST,
        RIGHT_WRIST,
        LEFT_HIP,
        RIGHT_HIP,
    ]

    valid_frames = []

    for frame in frames:
        landmarks = [
            _safe_landmark(frame, index)
            for index in required_landmarks
        ]

        if all(landmark is not None for landmark in landmarks):
            valid_frames.append(frame)

    # Require enough reliable frames.
    if len(valid_frames) < 15:
        return {
            "is_batting": False,
            "confidence": 0.15,
            "reason": (
                "Not enough clear body-pose frames were detected. "
                "Please upload a clear full-body video."
            ),
        }

    wrist_movements = []
    torso_movements = []
    relative_wrist_movements = []

    previous = None

    for frame in valid_frames:

        left_shoulder = frame[LEFT_SHOULDER]
        right_shoulder = frame[RIGHT_SHOULDER]

        left_wrist = frame[LEFT_WRIST]
        right_wrist = frame[RIGHT_WRIST]

        left_hip = frame[LEFT_HIP]
        right_hip = frame[RIGHT_HIP]

        shoulder_width = _distance(
            left_shoulder,
            right_shoulder
        )

        if shoulder_width < 0.02:
            continue

        shoulder_center = _midpoint(
            left_shoulder,
            right_shoulder
        )

        hip_center = _midpoint(
            left_hip,
            right_hip
        )

        current = {
            "left_wrist": left_wrist,
            "right_wrist": right_wrist,
            "shoulder_center": shoulder_center,
            "hip_center": hip_center,
            "scale": shoulder_width,
        }

        if previous is not None:

            scale = max(
                (previous["scale"] + shoulder_width) / 2,
                0.02
            )

            left_motion = (
                _distance(
                    previous["left_wrist"],
                    left_wrist
                ) / scale
            )

            right_motion = (
                _distance(
                    previous["right_wrist"],
                    right_wrist
                ) / scale
            )

            torso_motion = (
                _distance(
                    previous["shoulder_center"],
                    shoulder_center
                ) / scale
            )

            # Use the larger wrist movement for this frame.
            wrist_motion = max(
                left_motion,
                right_motion
            )

            wrist_movements.append(wrist_motion)
            torso_movements.append(torso_motion)

            relative_wrist_movements.append(
                max(
                    0.0,
                    wrist_motion - torso_motion
                )
            )

        previous = current

    if len(wrist_movements) < 10:
        return {
            "is_batting": False,
            "confidence": 0.20,
            "reason": (
                "Not enough movement data was available "
                "for reliable validation."
            ),
        }

    # ---------------------------------------------------------
    # ROBUST MOVEMENT MEASUREMENTS
    # ---------------------------------------------------------

    median_wrist_motion = statistics.median(
        wrist_movements
    )

    median_torso_motion = statistics.median(
        torso_movements
    )

    median_relative_motion = statistics.median(
        relative_wrist_movements
    )

    # Instead of using ONE extreme frame, count how many
    # frames contain meaningful wrist movement.
    active_frames = sum(
        1
        for value in wrist_movements
        if value > 0.08
    )

    activity_ratio = (
        active_frames / len(wrist_movements)
    )

    # ---------------------------------------------------------
    # BATTING-LIKE MOVEMENT SCORE
    # ---------------------------------------------------------

    score = 0.0

    # 1. Sustained wrist movement.
    # This is much more important than one huge movement.
    if median_wrist_motion >= 0.40:
        score += 0.35
    elif median_wrist_motion >= 0.20:
        score += 0.25
    elif median_wrist_motion >= 0.12:
        score += 0.15

    # 2. Movement should continue across a meaningful
    # portion of the video.
    if activity_ratio >= 0.60:
        score += 0.30
    elif activity_ratio >= 0.40:
        score += 0.15

    # 3. Wrist movement should be greater than torso movement.
    if median_relative_motion >= 0.08:
        score += 0.20
    elif median_relative_motion >= 0.04:
        score += 0.10

    # 4. Avoid treating large whole-body movement as batting.
    if median_torso_motion < 0.15:
        score += 0.15

    score = min(score, 1.0)

    # ---------------------------------------------------------
    # FINAL DECISION
    # ---------------------------------------------------------

    is_batting = (
        score >= 0.55
        and median_wrist_motion >= 0.12
        and activity_ratio >= 0.25
    )

    if is_batting:
        reason = (
            "Sustained batting-like upper-body movement "
            "was detected."
        )
    else:
        reason = (
            "The video does not show enough sustained "
            "batting-like movement."
        )

    return {
        "is_batting": is_batting,
        "confidence": round(score, 2),
        "reason": reason,
        "diagnostics": {
            "valid_pose_frames": len(valid_frames),
            "activity_ratio": round(activity_ratio, 3),
            "median_wrist_motion": round(
                median_wrist_motion, 3
            ),
            "median_torso_motion": round(
                median_torso_motion, 3
            ),
            "median_relative_motion": round(
                median_relative_motion, 3
            ),
        },
    }
def clamp(value, low=0, high=100):
    return max(low, min(high, value))

def calculate_scores(features):
    """
    Educational heuristic scoring for the MVP.
    These are not clinically/professionally validated scores.
    """

    # Knee score: moderate bend is preferred for a generic batting stance.
    knee_avg = (
        features["left_knee_angle"] + features["right_knee_angle"]
    ) / 2
    knee_score = 100 - abs(knee_avg - 155) * 1.2

    # Elbow score: a broad target range for a general batting movement.
    elbow_avg = (
        features["left_elbow_angle"] + features["right_elbow_angle"]
    ) / 2
    elbow_score = 100 - abs(elbow_avg - 145) * 0.9

    # Lower shoulder tilt is treated as better stability.
    shoulder_score = 100 - features["shoulder_tilt_average"] * 180

    # Lower head vertical movement is treated as better stability.
    head_score = 100 - features["head_vertical_movement"] * 250

    return {
        "balance": round(clamp((knee_score + shoulder_score) / 2)),
        "head_stability": round(clamp(head_score)),
        "arm_position": round(clamp(elbow_score)),
        "lower_body": round(clamp(knee_score)),
    }

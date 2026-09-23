import math

def calculate_angle(a, b, c):
    """
    Returns angle ABC in degrees.
    Each point is a dict/object with x and y attributes/keys.
    """
    ax, ay = a["x"], a["y"]
    bx, by = b["x"], b["y"]
    cx, cy = c["x"], c["y"]

    ba = (ax - bx, ay - by)
    bc = (cx - bx, cy - by)

    dot = ba[0] * bc[0] + ba[1] * bc[1]
    mag_ba = math.hypot(*ba)
    mag_bc = math.hypot(*bc)

    if mag_ba == 0 or mag_bc == 0:
        return 0.0

    cosine = max(-1.0, min(1.0, dot / (mag_ba * mag_bc)))
    return math.degrees(math.acos(cosine))

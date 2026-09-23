def generate_feedback(scores):
    feedback = []

    if scores["head_stability"] < 60:
        feedback.append(
            "Your head movement appears relatively high. Work on keeping your head "
            "stable and balanced through the shot."
        )
    else:
        feedback.append("Head stability looks reasonably consistent in this video.")

    if scores["lower_body"] < 60:
        feedback.append(
            "Your lower-body measurements vary from the project's target range. "
            "Practice a stable base and controlled front-foot movement."
        )
    else:
        feedback.append("Lower-body positioning looks reasonably controlled.")

    if scores["arm_position"] < 60:
        feedback.append(
            "Arm-angle measurements vary from the target range. Review your bat-arm "
            "position with a coach and repeat the drill slowly."
        )
    else:
        feedback.append("Arm positioning looks reasonably consistent.")

    if scores["balance"] < 60:
        feedback.append(
            "Focus on maintaining balance from setup through follow-through."
        )
    else:
        feedback.append("Overall balance indicators look reasonably stable.")

    feedback.append(
        "For accurate cricket coaching, compare this report with an experienced "
        "coach and use consistent camera angles when recording future videos."
    )

    return feedback

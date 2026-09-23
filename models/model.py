from sklearn.ensemble import RandomForestClassifier

def build_demo_model():
    """
    Placeholder model factory.
    A real shot classifier should be trained after collecting
    labeled cricket-video features.
    """
    return RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

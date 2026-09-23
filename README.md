# AI Cricket Coach

An educational AI-assisted cricket batting technique analyzer.

## Current MVP

The first version:
1. Uploads a batting video.
2. Uses MediaPipe pose landmarks.
3. Extracts basic body measurements.
4. Calculates simple technique indicators.
5. Produces scores and coaching-oriented feedback.

## Important scope

This is a college-project prototype, not a professional coaching or medical system. The scores are heuristic until a labeled cricket dataset is collected and a trained ML model is added.

## Run

```bash
python -m venv venv
# Windows:
venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

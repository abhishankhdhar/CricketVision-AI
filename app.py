import tempfile
import streamlit as st

from core.video_processor import save_uploaded_video, analyze_video
from core.batting_validator import validate_batting_video
from analysis.technique_analyzer import analyze_technique
from analysis.score_calculator import calculate_scores
from analysis.feedback_generator import generate_feedback
from ai.gemini_assistant import ask_gemini


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Cricket Coach",
    page_icon="🏏",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🏏 AI Cricket Coach")

st.caption(
    "AI-assisted batting technique analysis using "
    "computer vision and pose landmarks."
)


# ============================================================
# VIDEO UPLOAD
# ============================================================

uploaded = st.file_uploader(
    "Upload a batting video",
    type=["mp4", "mov", "avi"]
)


if uploaded:

    # Create temporary directory for uploaded video
    temp_dir = tempfile.mkdtemp(
        prefix="cricket_coach_"
    )

    video_path = save_uploaded_video(
        uploaded,
        temp_dir
    )

    # Display uploaded video
    st.video(video_path)


    # ========================================================
    # ANALYZE BUTTON
    # ========================================================

    if st.button(
        "🔍 Analyze Batting Technique",
        type="primary"
    ):

        # Remove previous analysis before analyzing
        # a new video.
        st.session_state.pop("result", None)
        st.session_state["chat_history"] = []

        with st.spinner(
            "🏏 Processing video and checking batting action..."
        ):

            try:

                # ------------------------------------------------
                # STEP 1: Extract pose landmarks
                # ------------------------------------------------

                landmarks = analyze_video(
                    video_path
                )


                # ------------------------------------------------
                # STEP 2: Validate whether video contains
                # a batting-like action
                # ------------------------------------------------

                validation = validate_batting_video(
                    landmarks
                )


                # ------------------------------------------------
                # STEP 3: Reject non-batting videos
                # ------------------------------------------------

                if not validation["is_batting"]:

                    st.error(
                        "❌ This does not appear to be a "
                        "cricket batting video."
                    )

                    st.info(
                        "Please upload a clear video of a player "
                        "performing a batting shot."
                    )

                    # Show useful validation information
                    st.caption(
                        f"Validation confidence: "
                        f"{validation['confidence']}"
                    )

                    st.stop()


                # ------------------------------------------------
                # STEP 4: Batting video detected
                # ------------------------------------------------

                st.success(
                    "✅ Batting action detected. "
                    "Starting technique analysis..."
                )


                # ------------------------------------------------
                # STEP 5: Analyze batting technique
                # ------------------------------------------------

                technique = analyze_technique(
                    landmarks
                )


                # ------------------------------------------------
                # STEP 6: Calculate technique scores
                # ------------------------------------------------

                scores = calculate_scores(
                    technique
                )


                # ------------------------------------------------
                # STEP 7: Generate coaching feedback
                # ------------------------------------------------

                feedback = generate_feedback(
                    scores
                )


                # ------------------------------------------------
                # STEP 8: Store analysis result
                # ------------------------------------------------

                st.session_state["result"] = {
                    "technique": technique,
                    "scores": scores,
                    "feedback": feedback,
                    "validation": validation,
                }


                # Start a fresh AI chat for the new analysis
                st.session_state["chat_history"] = []


                st.success(
                    "Batting analysis completed successfully! 🏏"
                )


            except Exception as exc:

                st.error(
                    f"Analysis failed: {exc}"
                )


# ============================================================
# ANALYSIS REPORT
# ============================================================

if "result" in st.session_state:

    result = st.session_state["result"]

    scores = result["scores"]


    st.divider()

    st.header("📊 Analysis Report")


    # --------------------------------------------------------
    # Technique Scores
    # --------------------------------------------------------

    cols = st.columns(
        len(scores)
    )


    for col, (name, value) in zip(
        cols,
        scores.items()
    ):

        col.metric(
            name.replace(
                "_",
                " "
            ).title(),

            f"{value}/100"
        )


    # --------------------------------------------------------
    # Coaching Feedback
    # --------------------------------------------------------

    st.subheader(
        "📝 Coaching Feedback"
    )


    for item in result["feedback"]:

        st.write(
            f"• {item}"
        )


    # --------------------------------------------------------
    # Technical Measurements
    # --------------------------------------------------------

    st.subheader(
        "🔎 Technical Measurements"
    )


    st.json(
        result["technique"]
    )


# ============================================================
# AI CRICKET ASSISTANT
# ============================================================

st.divider()

st.header(
    "🤖 Ask Cricket AI"
)


st.caption(
    "Ask questions about your batting technique, "
    "training drills, cricket skills, or cricket information."
)


# ============================================================
# CREATE CHAT HISTORY
# ============================================================

if "chat_history" not in st.session_state:

    st.session_state["chat_history"] = []


# ============================================================
# DISPLAY PREVIOUS CHAT MESSAGES
# ============================================================

for message in st.session_state["chat_history"]:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask something like: How can I improve my head stability?"
)


if question:

    # --------------------------------------------------------
    # Show user message
    # --------------------------------------------------------

    st.session_state["chat_history"].append(
        {
            "role": "user",
            "content": question
        }
    )


    with st.chat_message("user"):

        st.markdown(
            question
        )


    # --------------------------------------------------------
    # Get current batting analysis
    # --------------------------------------------------------

    analysis_context = None


    if "result" in st.session_state:

        analysis_context = (
            st.session_state["result"]
        )


    # --------------------------------------------------------
    # OpenRouter AI Assistant
    # --------------------------------------------------------

    try:

        api_key = st.secrets[
            "OPENROUTER_API_KEY"
        ]


        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "🏏 Cricket AI is thinking..."
            ):

                answer = ask_gemini(
                    question=question,
                    analysis=analysis_context,
                    api_key=api_key
                )


                st.markdown(
                    answer
                )


        # ----------------------------------------------------
        # Save AI response
        # ----------------------------------------------------

        st.session_state["chat_history"].append(
            {
                "role": "assistant",
                "content": answer
            }
        )


    except Exception as exc:

        st.error(
            f"Unable to contact Cricket AI: {exc}"
        )
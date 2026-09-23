import tempfile
import streamlit as st

from core.video_processor import save_uploaded_video, analyze_video
from analysis.technique_analyzer import analyze_technique
from analysis.score_calculator import calculate_scores
from analysis.feedback_generator import generate_feedback
from ai.gemini_assistant import ask_gemini


st.set_page_config(
    page_title="AI Cricket Coach",
    page_icon="🏏",
    layout="wide"
)

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

    temp_dir = tempfile.mkdtemp(
        prefix="cricket_coach_"
    )

    video_path = save_uploaded_video(
        uploaded,
        temp_dir
    )

    st.video(video_path)


    if st.button(
        "🔍 Analyze Batting Technique",
        type="primary"
    ):

        with st.spinner(
            "🏏 Analyzing batting technique..."
        ):

            try:

                landmarks = analyze_video(
                    video_path
                )

                technique = analyze_technique(
                    landmarks
                )

                scores = calculate_scores(
                    technique
                )

                feedback = generate_feedback(
                    scores
                )


                st.session_state["result"] = {
                    "technique": technique,
                    "scores": scores,
                    "feedback": feedback,
                }


                # Start a fresh chat after a new analysis
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


    st.subheader(
        "📝 Coaching Feedback"
    )


    for item in result["feedback"]:

        st.write(
            f"• {item}"
        )


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


# Create chat history if it doesn't exist

if "chat_history" not in st.session_state:

    st.session_state["chat_history"] = []


# Display previous messages

for message in st.session_state["chat_history"]:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# Chat input

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
    # OpenRouter
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


        # Save AI response

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
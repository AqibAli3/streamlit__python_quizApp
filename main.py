import streamlit as st
import json
import random
import base64
import time
import streamlit.components.v1 as components

# Total time for the quiz (25 minutes = 1500 seconds)
TOTAL_TIME = 1500

# Set page configuration (must be at the very top)
st.set_page_config(
    page_title="Python MCQ Quiz App",  # Browser tab title
    page_icon="📝",                    # Favicon (can be an emoji)
    layout="wide",                     # Wide layout for better display
    initial_sidebar_state="collapsed"  # Collapse sidebar by default
)

# ----------------------------------
# Inject meta tags to set preview data (title image, title, and description)
def set_meta_tags():
    meta_html = f"""
    <html>
      <head>
        <meta property="og:image" content="https://www.shutterstock.com/image-photo/businesswomen-tick-mark-assessment-questionnaire-600nw-2477971423.jpg">
        <meta property="og:title" content="Python MCQ Quiz App">
        <meta property="og:description" content="Test your knowledge with our interactive Python quiz!">
      </head>
      <body></body>
    </html>
    """
    # Use an invisible HTML component to inject meta tags.
    components.html(meta_html, height=0, width=0)

# ----------------------------------
# Function to set the background image using imag.png.
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# ----------------------------------
# Function to set custom CSS with standard sizes for fonts and spacing,
# and to center-align all content in the view.
def set_custom_css():
    css = """
    <style>
    /* Base font settings */
    html {
        font-size: 16px;
    }
    body {
        font-family: Arial, sans-serif;
        font-size: 1rem;
        line-height: 1.5;
        color: #333;
        text-align: center; /* Center all text by default */
    }
    /* Headings */
    h1 { font-size: 2rem; }
    h2 { font-size: 1.75rem; }
    h3 { font-size: 1.5rem; }
    /* Standard elements */
    .stMarkdown, .stText, .stTextInput, .stButton, .stNumberInput {
        font-size: 1rem;
    }
    /* Prominent question text styling */
    .question-text {
        font-size: 1.25rem;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 1px 1px 2px #000;
        padding: 0.625rem;
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 0.3125rem;
        margin: 0.625rem 0;
    }
    /* Button styling */
    .stButton > button {
        font-size: 1rem;
        padding: 0.5rem 1rem;
    }
    /* Input fields styling */
    .stTextInput > div > input,
    .stNumberInput > div > input {
        font-size: 1rem;
        padding: 0.5rem;
    }
    /* Center radio button groups */
    div[role="radiogroup"] {
         display: flex;
         flex-direction: column;
         align-items: center;
    }
    /* Center the main container */
    div.block-container {
         margin-left: auto;
         margin-right: auto;
         text-align: center;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ----------------------------------
# Function to load questions from questions.json file.
def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
        return questions
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return []

# ----------------------------------
# Function to render a percentage circle using SVG.
def render_progress_circle(percentage):
    if percentage <= 35:
        color = "#ff0000"  # Red
    elif percentage <= 60:
        color = "#FFD700"  # Yellow/gold
    else:
        color = "#008000"  # Green
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; margin: 1.25rem 0;">
      <svg width="158" height="158" viewBox="0 0 36 36" class="circular-chart">
        <path class="circle-bg" 
              d="M18 2.0845
                 a 15.9155 15.9155 0 0 1 0 31.831
                 a 15.9155 15.9155 0 0 1 0 -31.831"
              style="fill:none;stroke:#eee;stroke-width:3;"></path>
        <path class="circle"
              d="M18 2.0845
                 a 15.9155 15.9155 0 0 1 0 31.831
                 a 15.9155 15.9155 0 0 1 0 -31.831"
              style="fill:none;stroke:{color};stroke-width:3;
                     stroke-dasharray: {percentage}, 100;
                     stroke-dashoffset: 0;
                     transition: stroke-dasharray 0.6s ease;"></path>
        <text x="18" y="20.35" style="fill:#666; font-size:0.4375rem; text-anchor:middle;">{percentage}%</text>
      </svg>
    </div>
    """
    return html

# ----------------------------------
# Function to display the timer on every page once the quiz starts.
def display_timer():
    if "quiz_start_time" in st.session_state:
        elapsed = time.time() - st.session_state["quiz_start_time"]
        remaining = TOTAL_TIME - elapsed
        if remaining < 0:
            remaining = 0
        mins = int(remaining // 60)
        secs = int(remaining % 60)
        st.markdown(
            f"<div style='text-align: center; font-size: 1rem; color: #333;'>"
            f"<strong>Time Remaining: {mins:02d}:{secs:02d}</strong></div>",
            unsafe_allow_html=True
        )
        if remaining <= 0:
            st.error("Time's up! The quiz will now end automatically.")
            st.session_state["current_index"] = len(st.session_state.get("questions", []))
            st.experimental_rerun()

# Call our meta tag injection once.
set_meta_tags()
# ----------------------------------
# Welcome screen – collects name and roll number.
def welcome():
    with st.container():
        st.title("Python MCQ Quiz App")
        st.header("Welcome!")
        st.write("Please enter your details to start the quiz.")
        with st.form(key="welcome_form"):
            name = st.text_input("Enter your name:")
            roll_input = st.text_input("Enter your roll number:")
            submitted = st.form_submit_button("Submit Details")
            if submitted:
                if not name.strip():
                    st.error("Name cannot be empty.")
                elif not name.replace(" ", "").isalpha():
                    st.error("Name can only contain alphabetic characters and spaces.")
                elif not roll_input.strip():
                    st.error("Roll number cannot be empty.")
                elif not roll_input.strip().isdigit():
                    st.error("Roll number must be numeric.")
                elif int(roll_input.strip()) == 0:
                    st.error("Roll number cannot be 0.")
                else:
                    st.session_state["name"] = name
                    st.session_state["roll"] = int(roll_input.strip())
                    st.session_state["quiz_started"] = True
                    # Record quiz start time.
                    st.session_state["quiz_start_time"] = time.time()
                    questions = load_questions()
                    if questions:
                        st.session_state["questions"] = random.sample(questions, k=min(20, len(questions)))
                    else:
                        st.session_state["questions"] = []
                    st.session_state["current_index"] = 0
                    st.session_state["score"] = 0

# ----------------------------------
# Quiz screen – displays one question at a time.
def quiz():
    display_timer()
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index+1} of {len(questions)}")
        st.markdown(
            f"<div class='question-text'>{question['question']}</div>", 
            unsafe_allow_html=True
        )
        
        submitted_key = f"submitted_{current_index}"
        if submitted_key not in st.session_state:
            # Use a placeholder so that no valid option is pre-selected.
            answer = st.radio(
                "Select your answer:",
                options=["Select an option"] + question["options"],
                key=f"q{current_index}"
            )
            if st.button("Submit Answer", key=f"submit_{current_index}"):
                if answer == "Select an option":
                    st.error("Please select a valid option before submitting.")
                else:
                    st.session_state[submitted_key] = answer
                    if answer == question["answer"]:
                        st.session_state["score"] += 1
        else:
            answer = st.session_state[submitted_key]
            st.write(f"Your Answer: **{answer}**")
            if answer == question["answer"]:
                st.success("Correct Answer!")
            else:
                st.error(f"Wrong Answer! Correct Answer is: **{question['answer']}**")
            # For the last question, show "Check Result"; otherwise "Next Question".
            if current_index == len(questions) - 1:
                if st.button("Check Result", key="check_result"):
                    st.session_state["current_index"] = current_index + 1
            else:
                if st.button("Next Question", key=f"next_{current_index}"):
                    st.session_state["current_index"] = current_index + 1
    else:
        result()

# ----------------------------------
# Result screen – displays final score, percentage, and a progress circle.
def result():
    display_timer()
    st.title("Quiz Completed!")
    st.write(f"Name: {st.session_state.get('name', 'N/A')}")
    st.write(f"Roll Number: {st.session_state.get('roll', 'N/A')}")
    
    score = st.session_state.get("score", 0)
    total = len(st.session_state.get("questions", []))
    percentage = int((score / total) * 100) if total > 0 else 0
    
    st.write(f"Your score: {score} out of {total}")
    st.write(f"Percentage: {percentage}%")
    
    circle_html = render_progress_circle(percentage)
    st.markdown(circle_html, unsafe_allow_html=True)
    
    if percentage <= 35:
        st.error("Result: Poor, try again!")
    elif percentage <= 60:
        st.warning("Result: Average performance!")
    else:
        st.success("Result: Well done!")
    
    if st.button("Try Again"):
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score", "quiz_start_time"]:
            if key in st.session_state:
                del st.session_state[key]

# ----------------------------------
# Main function – decides which screen (welcome, quiz, or result) to display.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()

# Python MCQ Quiz App

This is a Streamlit-based Python quiz application designed for a multiple-choice quiz. Users enter their name and roll number to begin the quiz, and questions are loaded from a `questions.json` file. The app includes a 25-minute countdown timer that, when expired, automatically ends the quiz (unanswered questions are marked incorrect) and displays the results. The results page shows your score, percentage, and a progress circle that visually represents your performance.

## Features

- **User Input Page:**  
  Users provide their name and roll number before starting the quiz.

- **Dynamic Quiz Screen:**  
  Questions are displayed one-by-one with answer options loaded from `questions.json`.

- **Countdown Timer:**  
  A 25-minute timer is shown on every quiz and result page. Once time expires, the quiz auto-skips remaining questions and ends the session.

- **Results Display:**  
  The results page shows:
  - Total score
  - Percentage of correct answers
  - A progress circle (color-coded based on performance)

- **Custom Styling:**  
  The app uses a custom background (`imag.png`) with CSS styling tailored for a clean and responsive user interface.

- **Deployment Ready:**  
  Easily deployable on Streamlit Cloud. You can keep your GitHub repository private and still deploy your app publicly.

## Prerequisites

- Python 3.7 or higher
- [Streamlit](https://streamlit.io/)
Today
need to some chages when i click submit question
Below is an updated version of your Streamlit app code. In this update, when the user clicks the "Submit Answer" button, the app will:

• Store the user’s choice for that question. • Display feedback (correct/incorrect) immediately. • Replace the answer radio buttons and submit button with a "Next Question" button so that the user can review the feedback before moving on.

Save this code as your app.py file (ensure you have your imag.png and questions.json in the same folder), then run it with:

bash
streamlit run app.py
python
import streamlit as st
import json
import random
import base64

# Function to set the background image
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# Function to set custom CSS to adjust text sizes (for questions, etc.)
def set_custom_css():
    css = """
    <style>
    /* Responsive question text size based on viewport width */
    .question-text {
        font-size: calc(16px + 1vw);
        font-weight: bold;
        margin: 10px 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Function to load questions from questions.json file
def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
        return questions
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return []

# Welcome screen to collect user details
def welcome():
    st.title("Python MCQ Quiz App")
    st.header("Welcome!")
    st.write("Please enter your details to start the quiz.")
    
    # User inputs
    name = st.text_input("Enter your name:")
    roll = st.text_input("Enter your roll number:")
    
    if st.button("Start Quiz"):
        if name and roll:
            # Set session state variables
            st.session_state["name"] = name
            st.session_state["roll"] = roll
            st.session_state["quiz_started"] = True
            
            # Load questions and randomly pick up to 20 questions
            questions = load_questions()
            if questions:
                st.session_state["questions"] = random.sample(questions, k=min(20, len(questions)))
            else:
                st.session_state["questions"] = []
            st.session_state["current_index"] = 0
            st.session_state["score"] = 0
        else:
            st.error("Please enter both your name and roll number.")

# Quiz screen to display questions one-by-one with controlled submit behavior
def quiz():
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        # Use a unique key to track submission for this question
        submitted_key = f"submitted_{current_index}"
        
        # If the question has NOT been submitted yet, show the answer options & submit button
        if submitted_key not in st.session_state:
            user_answer = st.radio("Select your answer:", question["options"], key=f"q{current_index}")
            
            if st.button("Submit Answer", key=f"submit_{current_index}"):
                # Store the submitted answer in session state
                st.session_state[submitted_key] = user_answer
                # Update score only once upon submission
                if user_answer == question["answer"]:
                    st.session_state["score"] += 1
        else:
            # If already submitted: show the submitted answer and feedback
            user_answer = st.session_state[submitted_key]
            if user_answer == question["answer"]:
                st.success("Correct answer!")
            else:
                st.error(f"Wrong answer! The correct answer is: {question['answer']}")
            
            # Show a 'Next Question' button to proceed after reviewing feedback
            if st.button("Next Question", key=f"next_{current_index}"):
                st.session_state["current_index"] = current_index + 1
                # No explicit rerun function is needed; widget interaction triggers a re-run naturally.
    else:
        result()  # All questions completed, show result

# Result screen to display final score and percentage
def result():
    st.title("Quiz Completed!")
    st.write(f"Name: {st.session_state.get('name', 'N/A')}")
    st.write(f"Roll Number: {st.session_state.get('roll', 'N/A')}")
    
    score = st.session_state.get("score", 0)
    total = len(st.session_state.get("questions", []))
    percentage = (score / total) * 100 if total > 0 else 0
        
    st.write(f"Your score: {score} out of {total}")
    st.write(f"Percentage: {percentage:.2f}%")
    
    if percentage < 33:
        st.error("Result: Poor, try again!")
    elif percentage < 60:
        st.warning("Result: Average performance!")
    else:
        st.success("Result: Well done!")
    
    if st.button("Try Again"):
        # Clear session state to restart quiz
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# Main function to drive the app
def main():
    # Set background image and custom CSS
    set_background("imag.png")
    set_custom_css()
    
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
What Changed on "Submit Answer"
Submission Handling:

A key (submitted_{current_index}) is stored in st.session_state when the user clicks "Submit Answer".

Until the answer is submitted, the radio buttons and Submit Answer button are displayed.

Feedback & Next Button:

After submission, the app shows feedback (using st.success or st.error) and disables the original answer selection.

A "Next Question" button then appears. When the user clicks it, the app increments the question index, moving to the next question.

This update provides the user with clear feedback on their answer and control over when to proceed to the next question.

If you need further adjustments or additional features (such as animations or timed delays), please let me know!


showing error
Yeh error aapke app mein nahin balkay aapke questions.json file mein hai. Python ka json.load() function file ko parse karte waqt error de raha hai, iska matlab aapke JSON file mein koi syntax mistake hai—shayad koi missing comma, quotation mark ya koi extra character jo JSON format ke mutabiq nahin hai.

Solution ke liye kuch steps:

JSON File Ko Validate Karein: Aap apne questions.json file ka content copy karke JSONLint jaisi website par paste karein. Yeh tool aapko batayega ke file mein syntax error kaha hai (line 1912, column 5 ke aas paas).

Error Wali Line Ko Check Karein: Apne text editor (Notepad++, VSCode, etc.) mein questions.json file open karein aur line 1912 column 5 par dekhein. Ho sakta hai koi:

Missing comma (,) ho

Extra ya missing quotation marks ho

Ya koi bracket ({ ya ]) galat use hua ho

File Ko Correct Karein: Jo error indicator diya gaya hai, uss hisse ko theek kar dein. Agar aap confuse hain, to apne file ke uss hissa ko yahan paste karke expert se ya online validator se help le sakte hain.

Phir Se Run Karein: Jab file ko update kar lein aur valid JSON ho jaye, to phir se apne Streamlit app ko run karke dekhein:

bash
streamlit run app.py
Yeh error code ke andar nahin balkay aapki questions.json file mein hai. File ko theek tareeke se validate aur correct karne ke baad, aapki quiz sahi chalni chahiye.

Agar aapko aur koi madad chahiye to zaroor batayein!

muje kuch chnages karne hain ile me 1. sb se phele ek problem hai jum me submit karata hun to ek bar me na to roll number ur name submit hota ha na hi quetion me chata hun ek bar me hi dono submint hon ur jub niche answer ata ha to bhi me apna answer change kar sakta hun ye na ho ek bar me answer submit ho niche answer aye ur jb answer show ho jai to me phr apna option change na kar sako ur us time submit nai balke next ka buttton show hor phele ye changes karo phr batata hun agal cj=hange
Below is a complete revised code that implements the following changes as per your requirements:

Welcome Screen Changes: – Both name and roll number are entered and submitted together using a single form.

Quiz Question Screen Changes: – Each question is placed inside its own form with a radio button and a "Submit Answer" button. – Once the user submits an answer, that answer is locked (the radio isn’t shown again), feedback is displayed, and a "Next Question" button appears. – After submission, the user cannot change his answer.

Simply save the code as your app.py (make sure you have imag.png and a valid questions.json in the same folder) and run with:

bash
streamlit run app.py
python
import streamlit as st
import json
import random
import base64

# Function to set the background image using imag.png
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# Function to set custom CSS to adjust question text size
def set_custom_css():
    css = """
    <style>
    /* Responsive question text */
    .question-text {
        font-size: calc(16px + 1vw);
        font-weight: bold;
        margin: 10px 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Function to load questions from questions.json file
def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
        return questions
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return []

# Welcome screen: uses a form to submit both name and roll at once.
def welcome():
    st.title("Python MCQ Quiz App")
    st.header("Welcome!")
    st.write("Please enter your details to start the quiz.")
    
    with st.form(key="welcome_form"):
        name = st.text_input("Enter your name:")
        roll = st.text_input("Enter your roll number:")
        submitted = st.form_submit_button("Submit Details")
        if submitted:
            if name and roll:
                st.session_state["name"] = name
                st.session_state["roll"] = roll
                st.session_state["quiz_started"] = True
                questions = load_questions()
                if questions:
                    st.session_state["questions"] = random.sample(questions, k=min(20, len(questions)))
                else:
                    st.session_state["questions"] = []
                st.session_state["current_index"] = 0
                st.session_state["score"] = 0
            else:
                st.error("Please enter both your name and roll number.")

# Quiz screen: each question is shown in a form; once answer is submitted, it is locked.
def quiz():
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        # Use a form for the current question only if not yet submitted
        submitted_key = f"submitted_{current_index}"
        if submitted_key not in st.session_state:
            with st.form(key=f"form_q{current_index}"):
                user_answer = st.radio("Select your answer:", question["options"], key=f"radio_q{current_index}")
                submit_ans = st.form_submit_button("Submit Answer")
                if submit_ans:
                    st.session_state[submitted_key] = user_answer
                    if user_answer == question["answer"]:
                        st.session_state["score"] += 1
                    # After submission, the form will no longer be shown.
        else:
            # If answer is submitted, show feedback and lock the answer.
            user_answer = st.session_state[submitted_key]
            if user_answer == question["answer"]:
                st.success("Correct answer!")
            else:
                st.error(f"Wrong answer! The correct answer is: {question['answer']}")
            
            # Provide a Next Question button (do not allow changes now).
            if st.button("Next Question", key=f"next_{current_index}"):
                st.session_state["current_index"] = current_index + 1
                # The widget interaction will trigger a re-run naturally.
    else:
        result()

# Result screen: displays final score and percentage
def result():
    st.title("Quiz Completed!")
    st.write(f"Name: {st.session_state.get('name', 'N/A')}")
    st.write(f"Roll Number: {st.session_state.get('roll', 'N/A')}")
    
    score = st.session_state.get("score", 0)
    total = len(st.session_state.get("questions", []))
    percentage = (score / total) * 100 if total > 0 else 0
        
    st.write(f"Your score: {score} out of {total}")
    st.write(f"Percentage: {percentage:.2f}%")
    
    if percentage < 33:
        st.error("Result: Poor, try again!")
    elif percentage < 60:
        st.warning("Result: Average performance!")
    else:
        st.success("Result: Well done!")
    
    if st.button("Try Again"):
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# Main function to control which screen is shown
def main():
    set_background("imag.png")      # Set the background image from imag.png
    set_custom_css()                # Set custom styles
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
Roman Urdu Explanation
Welcome Screen (Form): – Ab aap ek form mein name aur roll number enter karen aur "Submit Details" button dabayen. – Is se dono fields ek saat submit ho jayengi.

Quiz Screen (Form per Question): – Har question ke liye ek form banaya gaya hai jismein aap answer select kar sakte hain. – Jab aap "Submit Answer" dabate hain, to aapka answer lock ho jata hai aur feedback show hoti hai (correct or wrong). – Iss ke baad "Next Question" ka button nazar aata hai, jis se aap agla sawal dekh sakte hain aur ab aap answer change nahin kar sakte.

Result Screen: – Quiz complete hone ke baad naam, roll number, score, aur percentage show hoti hai. – "Try Again" button se aap poori quiz reset kar sakte hain.

Ye code aapki requirements ke mutabiq changes apply karta hai. Agar is mein koi aur change chahiye ya koi masla ho to zaroor batayein!

why i need to click more than 1 time to perform any opration submit, next quetion etc 1 more thing when app showing correct answer question must be showing but i cant change in that time
Below is an updated version of your code that aims to make the interactions smoother so that you only need to click one time per operation (submit, next question, etc.). In this version:

The welcome screen still uses a form (so that name and roll number are submitted together).

The quiz screen no longer uses a form for each question; it simply shows the answer options (with a radio button) and a single "Submit Answer" button. Once the answer is submitted, it immediately locks the answer (displaying static text and feedback) so that the user cannot change it afterward. Then a "Next Question" button is shown.

Try saving the code as app.py (make sure that imag.png and questions.json are in the same folder) and run it with:

bash
streamlit run app.py
Here’s the updated code:

python
import streamlit as st
import json
import random
import base64

# Function to set the background image using imag.png
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# Function to set custom CSS (for responsive question text, etc.)
def set_custom_css():
    css = """
    <style>
    .question-text {
        font-size: calc(16px + 1vw);
        font-weight: bold;
        margin: 10px 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Function to load questions from questions.json file
def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
        return questions
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return []

# Welcome screen – using a form so that both name and roll number are submitted together.
def welcome():
    st.title("Python MCQ Quiz App")
    st.header("Welcome!")
    st.write("Please enter your details to start the quiz.")
    
    with st.form(key="welcome_form"):
        name = st.text_input("Enter your name:")
        roll = st.text_input("Enter your roll number:")
        submitted = st.form_submit_button("Submit Details")
        if submitted:
            if name and roll:
                st.session_state["name"] = name
                st.session_state["roll"] = roll
                st.session_state["quiz_started"] = True
                # Load questions and randomly select up to 20
                questions = load_questions()
                if questions:
                    st.session_state["questions"] = random.sample(questions, k=min(20, len(questions)))
                else:
                    st.session_state["questions"] = []
                st.session_state["current_index"] = 0
                st.session_state["score"] = 0
            else:
                st.error("Please enter both your name and roll number.")

# Quiz screen – each question is shown with a radio button and a Submit button.
# Once submitted, the answer gets locked and feedback is displayed along with one Next Question button.
def quiz():
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        
        # If the question has not been answered yet, show the radio selection and submit button.
        if submitted_key not in st.session_state:
            answer = st.radio("Select your answer:", question["options"], key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
                st.session_state[submitted_key] = answer
                if answer == question["answer"]:
                    st.session_state["score"] += 1
                # After clicking "Submit Answer", the app re-runs and the submitted answer is now locked.
        else:
            # The answer has been submitted -> lock the answer and show feedback.
            answer = st.session_state[submitted_key]
            st.write(f"Your Answer: **{answer}**")
            if answer == question["answer"]:
                st.success("Correct Answer!")
            else:
                st.error(f"Wrong Answer! Correct Answer is: **{question['answer']}**")
            
            # Provide a Next Question button.
            if st.button("Next Question", key=f"next_{current_index}"):
                st.session_state["current_index"] = current_index + 1
    else:
        result()  # When all questions are completed, show the result screen.

# Result screen – displays final score and percentage.
def result():
    st.title("Quiz Completed!")
    st.write(f"Name: {st.session_state.get('name', 'N/A')}")
    st.write(f"Roll Number: {st.session_state.get('roll', 'N/A')}")
    
    score = st.session_state.get("score", 0)
    total = len(st.session_state.get("questions", []))
    percentage = (score / total) * 100 if total > 0 else 0
        
    st.write(f"Your score: {score} out of {total}")
    st.write(f"Percentage: {percentage:.2f}%")
    
    if percentage < 33:
        st.error("Result: Poor, try again!")
    elif percentage < 60:
        st.warning("Result: Average performance!")
    else:
        st.success("Result: Well done!")
    
    if st.button("Try Again"):
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# Main function to control which screen to show.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
Explanation of the Changes
Single Click Operations: By removing the extra form wrappers in the quiz section, the operation now depends solely on a single click of the "Submit Answer" button. After the answer is submitted, feedback is displayed immediately, and only one click is needed on the "Next Question" button to proceed. This should solve the issue of requiring multiple clicks.

Locking the Answer: Once you click "Submit Answer," the selected answer is stored in st.session_state via a unique key (submitted_{current_index}). The radio selection is then replaced by a static text display of your answer along with the feedback (either a success or error message). The radio widget is no longer shown so you cannot change the answer at that time.

Next Question: Only one button ("Next Question") is provided to move on once you have seen the feedback—ensuring the operation is straightforward.

Give this version a try. If you still experience issues or need further adjustments, please let me know!

chnage make sure user can put ine name coulm only name and in roll number colum input onl number
Below is an updated version of your code where the welcome screen now enforces that the "Name" field accepts only alphabetic characters (spaces are allowed), and the "Roll Number" field accepts only numeric input. For the roll number, we use Streamlit’s st.number_input, which automatically restricts input to numbers. Also, the code displays an error message if the name contains any characters other than letters and spaces.

Save this code as your app.py file (make sure that imag.png and a valid questions.json are in the same folder) and then run with:

bash
streamlit run app.py
python
import streamlit as st
import json
import random
import base64

# Function to set the background image using imag.png
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# Function to set custom CSS (for responsive question text, etc.)
def set_custom_css():
    css = """
    <style>
    .question-text {
        font-size: calc(16px + 1vw);
        font-weight: bold;
        margin: 10px 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Function to load questions from questions.json file
def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
        return questions
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return []

# Welcome screen – using a form so that both name and roll number are submitted together,
# and validated: name accepts only letters & spaces, roll number is numeric.
def welcome():
    st.title("Python MCQ Quiz App")
    st.header("Welcome!")
    st.write("Please enter your details to start the quiz.")
    
    with st.form(key="welcome_form"):
        name = st.text_input("Enter your name:")
        roll = st.number_input("Enter your roll number:", min_value=0, step=1, format="%d")
        submitted = st.form_submit_button("Submit Details")
        
        if submitted:
            # Validate that name is not empty and contains only alphabets (spaces allowed)
            if not name.strip():
                st.error("Name cannot be empty.")
            elif not name.replace(" ", "").isalpha():
                st.error("Name can only contain alphabetic characters and spaces.")
            else:
                st.session_state["name"] = name
                st.session_state["roll"] = int(roll)
                st.session_state["quiz_started"] = True
                
                # Load questions and randomly select up to 20 questions
                questions = load_questions()
                if questions:
                    st.session_state["questions"] = random.sample(questions, k=min(20, len(questions)))
                else:
                    st.session_state["questions"] = []
                st.session_state["current_index"] = 0
                st.session_state["score"] = 0

# Quiz screen – each question is shown with an answer radio button and a Submit button.
# Once submitted, the answer gets locked and feedback is displayed along with a Next Question button.
def quiz():
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        
        # If the question hasn't been answered yet, display the options and the submit button.
        if submitted_key not in st.session_state:
            answer = st.radio("Select your answer:", question["options"], key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
                st.session_state[submitted_key] = answer
                if answer == question["answer"]:
                    st.session_state["score"] += 1
        else:
            # The answer was already submitted -- lock the answer and show feedback.
            answer = st.session_state[submitted_key]
            st.write(f"Your Answer: **{answer}**")
            if answer == question["answer"]:
                st.success("Correct Answer!")
            else:
                st.error(f"Wrong Answer! Correct Answer is: **{question['answer']}**")
            
            # Next Question button. Clicking it moves to the next question.
            if st.button("Next Question", key=f"next_{current_index}"):
                st.session_state["current_index"] = current_index + 1
    else:
        result()

# Result screen – displays final score and percentage.
def result():
    st.title("Quiz Completed!")
    st.write(f"Name: {st.session_state.get('name', 'N/A')}")
    st.write(f"Roll Number: {st.session_state.get('roll', 'N/A')}")
    
    score = st.session_state.get("score", 0)
    total = len(st.session_state.get("questions", []))
    percentage = (score / total) * 100 if total > 0 else 0
        
    st.write(f"Your score: {score} out of {total}")
    st.write(f"Percentage: {percentage:.2f}%")
    
    if percentage < 33:
        st.error("Result: Poor, try again!")
    elif percentage < 60:
        st.warning("Result: Average performance!")
    else:
        st.success("Result: Well done!")
    
    if st.button("Try Again"):
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# Main function – controls which screen to display.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
Explanation
Welcome Screen Changes:

Uses a single form (via st.form) so that both the name and roll number are submitted together.

The Name field uses st.text_input and then validates that, after stripping spaces, it is not empty and contains only alphabetic characters (using name.replace(" ", "").isalpha()).

The Roll Number field uses st.number_input which automatically accepts only numbers.

Quiz & Result Screens:

The rest of the code remains as before to show each question, lock the answer after submission, display immediate feedback, and then allow only one click on "Next Question" once the answer is locked.

Feel free to let me know if you need any further adjustments!

1. when i compleate all 20 questions do not show next quetion will be show check result and than result will be shown 2. in result page show a circle represnt my question if 100 percent acurate my question showing green (if percentage 1% to 35% showing red, is 35 to 60 showing yellow and if above 60 show green circle 3. give me a skip bton for quiz to skip quiz only during im testin this app befor public i will remove o comit out this function also tell me from which line to which line code onl se for for skip beua ill change after testing app
Below is your updated code with the following changes:

Final Question Behavior:  • When the user answers the 20th (last) question, instead of showing a "Next Question" button the app will now show a "Check Result" button. Once clicked, the results screen is shown.

Results Screen – Colored Circle:  • On the results page, a circle is displayed whose color depends on the percentage:   – Red if your score is 1% to 35% (percentage ≤ 35%),   – Yellow if your score is between 35% and 60% (35% < percentage ≤ 60%), and   – Green if above 60%.

Skip Button for Testing:  • A "Skip Quiz" button is added at the top of the quiz screen. When clicked, it immediately sets the current question index to the end (i.e. skips the remaining questions).  • Note: The skip button code is enclosed between the comments   # SKIP BUTTON START (for testing)   and   # SKIP BUTTON END  You can remove or comment out these lines when you’re ready for public release.

Simply save the code as app.py (with your imag.png and a valid questions.json in the same folder) and run with:

streamlit run app.py
python
import streamlit as st
import json
import random
import base64

# Function to set the background image using imag.png
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# Function to set custom CSS (for responsive question text, etc.)
def set_custom_css():
    css = """
    <style>
    .question-text {
        font-size: calc(16px + 1vw);
        font-weight: bold;
        margin: 10px 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Function to load questions from questions.json file
def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
        return questions
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return []

# Welcome screen – using a form so that both name and roll number are submitted together.
# The Name field accepts only alphabets (and spaces) and the Roll Number field uses a number input.
def welcome():
    st.title("Python MCQ Quiz App")
    st.header("Welcome!")
    st.write("Please enter your details to start the quiz.")
    
    with st.form(key="welcome_form"):
        name = st.text_input("Enter your name:")
        roll = st.number_input("Enter your roll number:", min_value=0, step=1, format="%d")
        submitted = st.form_submit_button("Submit Details")
        
        if submitted:
            if not name.strip():
                st.error("Name cannot be empty.")
            elif not name.replace(" ", "").isalpha():
                st.error("Name can only contain alphabetic characters and spaces.")
            else:
                st.session_state["name"] = name
                st.session_state["roll"] = int(roll)
                st.session_state["quiz_started"] = True
                questions = load_questions()
                if questions:
                    st.session_state["questions"] = random.sample(questions, k=min(20, len(questions)))
                else:
                    st.session_state["questions"] = []
                st.session_state["current_index"] = 0
                st.session_state["score"] = 0

# Quiz screen – displays one question at a time.
def quiz():
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    # SKIP BUTTON START (for testing purposes only)
    if st.button("Skip Quiz", key="skip_quiz"):
         st.session_state["current_index"] = len(questions)  # Skip all remaining questions.
         # The skip button function is defined between these comments.
    # SKIP BUTTON END

    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        
        if submitted_key not in st.session_state:
            answer = st.radio("Select your answer:", question["options"], key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
                st.session_state[submitted_key] = answer
                if answer == question["answer"]:
                    st.session_state["score"] += 1
        else:
            # Answer is locked; show the submitted answer and feedback.
            answer = st.session_state[submitted_key]
            st.write(f"Your Answer: **{answer}**")
            if answer == question["answer"]:
                st.success("Correct Answer!")
            else:
                st.error(f"Wrong Answer! Correct Answer is: **{question['answer']}**")
            
            # If this is the last question, show "Check Result".
            if current_index == len(questions) - 1:
                if st.button("Check Result", key="check_result"):
                    st.session_state["current_index"] = current_index + 1
            else:
                if st.button("Next Question", key=f"next_{current_index}"):
                    st.session_state["current_index"] = current_index + 1
    else:
        result()

# Result screen – shows final score, percentage, and a colored circle indicator.
def result():
    st.title("Quiz Completed!")
    st.write(f"Name: {st.session_state.get('name', 'N/A')}")
    st.write(f"Roll Number: {st.session_state.get('roll', 'N/A')}")
    
    score = st.session_state.get("score", 0)
    total = len(st.session_state.get("questions", []))
    percentage = (score / total) * 100 if total > 0 else 0
        
    st.write(f"Your score: {score} out of {total}")
    st.write(f"Percentage: {percentage:.2f}%")
    
    # Determine circle color based on percentage.
    if percentage <= 35:
        color = "red"
    elif percentage <= 60:
        color = "yellow"
    else:
        color = "green"
    # Display a colored circle using HTML.
    circle_html = f"""
    <div style="width:100px; height:100px; border-radius:50%; background-color:{color}; margin:auto;">
    </div>
    """
    st.markdown(circle_html, unsafe_allow_html=True)
    
    if percentage <= 35:
        st.error("Result: Poor, try again!")
    elif percentage <= 60:
        st.warning("Result: Average performance!")
    else:
        st.success("Result: Well done!")
    
    if st.button("Try Again"):
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# Main function to control which screen is shown.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
Explanation
Final Question Behavior: In the quiz() function, when the current question is the last one (i.e. current_index == len(questions) - 1), the button label is changed to "Check Result" instead of "Next Question". Pressing it increments the index past the total questions, switching to the result() view.

Result Circle: The result() function calculates the percentage and then sets the circle’s color:   • Red if percentage is ≤ 35%   • Yellow if percentage is between 35% and 60%   • Green if percentage is above 60% It then uses an HTML <div> styled as a circle to display this.

Skip Button for Testing: At the very top of the quiz() function, a "Skip Quiz" button is inserted. – SKIP BUTTON START and SKIP BUTTON END comments clearly mark the lines that implement the skip function. – When clicked, it sets st.session_state["current_index"] to the total number of questions, thus skipping the quiz and sending the user to the results screen.

You can remove or comment out the lines between these skip comments when you are ready for public deployment.

If you need any further adjustments, let me know!


this type of percentage circle i want
Below is your updated code with a custom percentage circle using an SVG that mimics the style you showed (with segmented progress and a percentage label inside). The following changes have been made in addition to your previous requirements:

Final Question Behavior: – When the user completes all 20 questions, the "Check Result" button is shown instead of "Next Question".

Percentage Circle in Results: – On the results page, an SVG-based circular progress indicator is displayed. It fills a percentage of the circle (using a stroke-dasharray) and its color changes based on the percentage:   • Red if ≤35%   • Yellow (gold) if >35% and ≤60%   • Green if >60% – The percentage is labeled inside the circle.

Skip Button for Testing: – A "Skip Quiz" button is present (wrapped between comments so you can easily remove it later).

Below the code, you'll also see a helper function render_progress_circle(percentage) that produces the SVG code. You can adjust the styling as needed.

Save the code as app.py (ensure you have imag.png and a valid questions.json in the same folder) then run:

bash
streamlit run app.py
python
import streamlit as st
import json
import random
import base64

# ----------------------------------
# Function to set the background image using imag.png
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# Function to set custom CSS (for responsive question text, etc.)
def set_custom_css():
    css = """
    <style>
    .question-text {
        font-size: calc(16px + 1vw);
        font-weight: bold;
        margin: 10px 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ----------------------------------
# Function to load questions from questions.json file
def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
        return questions
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return []

# ----------------------------------
# Percentage circle function using SVG.
def render_progress_circle(percentage):
    # Determine color based on percentage.
    if percentage <= 35:
        color = "#ff0000"  # Red
    elif percentage <= 60:
        color = "#FFD700"  # Yellow (gold)
    else:
        color = "#008000"  # Green
    # Using an SVG where the viewBox is 0 0 36 36.
    # The stroke-dasharray is set to "{percentage}, 100" so that the arc fills according to the percentage.
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; margin:20px;">
      <svg width="120" height="120" viewBox="0 0 36 36" class="circular-chart">
        <path class="circle-bg" 
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:#eee;stroke-width:3;"></path>
        <path class="circle"
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:{color};stroke-width:3;stroke-dasharray: {percentage}, 100;stroke-dashoffset: 0;transition: stroke-dasharray 0.6s ease;"></path>
        <text x="18" y="20.35" style="fill:#666; font-size:7px; text-anchor:middle;">{percentage}%</text>
      </svg>
    </div>
    """
    return html

# ----------------------------------
# Welcome screen – using a form so that both name and roll number are submitted together.
def welcome():
    st.title("Python MCQ Quiz App")
    st.header("Welcome!")
    st.write("Please enter your details to start the quiz.")
    
    with st.form(key="welcome_form"):
        name = st.text_input("Enter your name:")
        roll = st.number_input("Enter your roll number:", min_value=0, step=1, format="%d")
        submitted = st.form_submit_button("Submit Details")
        
        if submitted:
            if not name.strip():
                st.error("Name cannot be empty.")
            elif not name.replace(" ", "").isalpha():
                st.error("Name can only contain alphabetic characters and spaces.")
            else:
                st.session_state["name"] = name
                st.session_state["roll"] = int(roll)
                st.session_state["quiz_started"] = True
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
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    # SKIP BUTTON START (for testing purposes only)
    if st.button("Skip Quiz", key="skip_quiz"):
         st.session_state["current_index"] = len(questions)  # Skip all remaining questions.
    # SKIP BUTTON END

    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        
        if submitted_key not in st.session_state:
            answer = st.radio("Select your answer:", question["options"], key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
                st.session_state[submitted_key] = answer
                if answer == question["answer"]:
                    st.session_state["score"] += 1
        else:
            # The answer is locked; display the user's answer and feedback.
            answer = st.session_state[submitted_key]
            st.write(f"Your Answer: **{answer}**")
            if answer == question["answer"]:
                st.success("Correct Answer!")
            else:
                st.error(f"Wrong Answer! The correct answer is: **{question['answer']}**")
            
            # Show "Check Result" if this is the last question; otherwise, show "Next Question".
            if current_index == len(questions) - 1:
                if st.button("Check Result", key="check_result"):
                    st.session_state["current_index"] = current_index + 1
            else:
                if st.button("Next Question", key=f"next_{current_index}"):
                    st.session_state["current_index"] = current_index + 1
    else:
        result()

# ----------------------------------
# Result screen – displays the final score, percentage, and a percentage circle.
def result():
    st.title("Quiz Completed!")
    st.write(f"Name: {st.session_state.get('name', 'N/A')}")
    st.write(f"Roll Number: {st.session_state.get('roll', 'N/A')}")
    
    score = st.session_state.get("score", 0)
    total = len(st.session_state.get("questions", []))
    percentage = int((score / total) * 100) if total > 0 else 0
        
    st.write(f"Your score: {score} out of {total}")
    st.write(f"Percentage: {percentage}%")
    
    # Render the circular progress indicator.
    circle_html = render_progress_circle(percentage)
    st.markdown(circle_html, unsafe_allow_html=True)
    
    if percentage <= 35:
        st.error("Result: Poor, try again!")
    elif percentage <= 60:
        st.warning("Result: Average performance!")
    else:
        st.success("Result: Well done!")
    
    if st.button("Try Again"):
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# ----------------------------------
# Main function – determines which screen (welcome, quiz, or result) to show.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
Code Breakdown
Skip Button: Lines between # SKIP BUTTON START (for testing purposes only) and # SKIP BUTTON END implement the skip functionality. You can remove or comment out these lines before public release.

Final Question Handling: In the quiz() function, if the current question is the last one (current_index == len(questions) - 1), the button text changes to "Check Result". Otherwise, it shows "Next Question".

Percentage Circle: The function render_progress_circle(percentage) generates an SVG-based circular progress indicator. The stroke-dasharray is set based on the given percentage, and the circle’s color is adjusted according to your thresholds (red, yellow, green). This HTML is rendered in the result() function.

Feel free to test this implementation. If you need further adjustments or encounter any issues, just let me know!

1. when i open my qny quetions 1 field already slected showin in that quiton option no any option selected showing
Below is the updated full code. In the quiz() function, the radio widget now prepends a dummy option ("Select an option") so that no valid answer is pre‐selected. When the user clicks Submit Answer, if the dummy option is still selected, an error is shown asking the user to select a valid option. Once a valid answer is submitted, the answer is locked and feedback is provided.

Save the following code as your app.py file (and ensure that imag.png and a valid questions.json file are in the same folder), then run it with:

bash
streamlit run app.py
python
import streamlit as st
import json
import random
import base64

# ----------------------------------
# Function to set the background image using imag.png
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# ----------------------------------
# Function to set custom CSS (for responsive question text, etc.)
def set_custom_css():
    css = """
    <style>
    .question-text {
        font-size: calc(16px + 1vw);
        font-weight: bold;
        margin: 10px 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ----------------------------------
# Function to load questions from questions.json file
def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
        return questions
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return []

# ----------------------------------
# Percentage circle function using SVG.
def render_progress_circle(percentage):
    if percentage <= 35:
        color = "#ff0000"  # Red
    elif percentage <= 60:
        color = "#FFD700"  # Yellow (gold)
    else:
        color = "#008000"  # Green
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; margin:20px;">
      <svg width="120" height="120" viewBox="0 0 36 36" class="circular-chart">
        <path class="circle-bg" 
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:#eee;stroke-width:3;"></path>
        <path class="circle"
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:{color};stroke-width:3;stroke-dasharray: {percentage}, 100;stroke-dashoffset: 0;transition: stroke-dasharray 0.6s ease;"></path>
        <text x="18" y="20.35" style="fill:#666; font-size:7px; text-anchor:middle;">{percentage}%</text>
      </svg>
    </div>
    """
    return html

# ----------------------------------
# Welcome screen – using a form so that both name and roll number are submitted together.
def welcome():
    st.title("Python MCQ Quiz App")
    st.header("Welcome!")
    st.write("Please enter your details to start the quiz.")
    
    with st.form(key="welcome_form"):
        name = st.text_input("Enter your name:")
        roll = st.number_input("Enter your roll number:", min_value=0, step=1, format="%d")
        submitted = st.form_submit_button("Submit Details")
        
        if submitted:
            if not name.strip():
                st.error("Name cannot be empty.")
            elif not name.replace(" ", "").isalpha():
                st.error("Name can only contain alphabetic characters and spaces.")
            else:
                st.session_state["name"] = name
                st.session_state["roll"] = int(roll)
                st.session_state["quiz_started"] = True
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
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    # SKIP BUTTON START (for testing purposes only)
    if st.button("Skip Quiz", key="skip_quiz"):
         st.session_state["current_index"] = len(questions)  # Skip all remaining questions.
    # SKIP BUTTON END
    
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        
        # If answer hasn't been submitted, show a radio widget with a dummy first option.
        if submitted_key not in st.session_state:
            # Prepend a dummy value so that no valid answer is pre-selected.
            options = ["Select an option"] + question["options"]
            # Set index=0 so that the dummy value is selected by default.
            answer = st.radio("Select your answer:", options, index=0, key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
                if answer == "Select an option":
                    st.error("Please select a valid option.")
                else:
                    st.session_state[submitted_key] = answer
                    if answer == question["answer"]:
                        st.session_state["score"] += 1
        else:
            # If the answer is already submitted, lock it and show feedback.
            answer = st.session_state[submitted_key]
            st.write(f"Your Answer: **{answer}**")
            if answer == question["answer"]:
                st.success("Correct Answer!")
            else:
                st.error(f"Wrong Answer! Correct Answer is: **{question['answer']}**")
            
            # Show "Check Result" on the last question; otherwise, "Next Question".
            if current_index == len(questions) - 1:
                if st.button("Check Result", key="check_result"):
                    st.session_state["current_index"] = current_index + 1
            else:
                if st.button("Next Question", key=f"next_{current_index}"):
                    st.session_state["current_index"] = current_index + 1
    else:
        result()

# ----------------------------------
# Result screen – displays the final score, percentage, and a percentage circle.
def result():
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
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# ----------------------------------
# Main function – decides which screen to display.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
Explanation of the Changes
No Pre-selected Option: In the quiz() function, the radio widget is now built from a list called options that starts with "Select an option" followed by the actual choices. Using index=0 makes the dummy option selected by default. When Submit Answer is clicked, the code checks if the answer is equal to "Select an option" and, if so, displays an error so the user must choose a valid answer.

Other Features:

The welcome and quiz logic, skip button, and result with an SVG-based percentage circle remain as before.

This should ensure that when a question is loaded, no valid answer is pre-selected. If you have further changes or questions, please let me know!

i do not want - + option in role number also not want ritten 0 in role number field
Below is the updated code where the roll number input is switched from a number input (which shows the “+” and “–” buttons and defaults to 0) to a text input. In the welcome screen, the roll number field now accepts a string; we then validate that it is numeric and not equal to 0. This way, no pre-filled 0 or plus/minus buttons appear.

You can replace the old welcome() function with the following updated version (the changes are within this function):

python
# Welcome screen – using a form so that both name and roll number are submitted together.
def welcome():
    st.title("Python MCQ Quiz App")
    st.header("Welcome!")
    st.write("Please enter your details to start the quiz.")
    
    with st.form(key="welcome_form"):
        name = st.text_input("Enter your name:")
        # Replacing st.number_input with st.text_input for roll number.
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
                questions = load_questions()
                if questions:
                    st.session_state["questions"] = random.sample(questions, k=min(20, len(questions)))
                else:
                    st.session_state["questions"] = []
                st.session_state["current_index"] = 0
                st.session_state["score"] = 0
For your convenience, here is the entire updated code with the new welcome() function included:

python
import streamlit as st
import json
import random
import base64

# ----------------------------------
# Function to set the background image using imag.png
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# ----------------------------------
# Function to set custom CSS (for responsive question text, etc.)
def set_custom_css():
    css = """
    <style>
    .question-text {
        font-size: calc(16px + 1vw);
        font-weight: bold;
        margin: 10px 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ----------------------------------
# Function to load questions from questions.json file
def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
        return questions
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return []

# ----------------------------------
# Percentage circle function using SVG.
def render_progress_circle(percentage):
    if percentage <= 35:
        color = "#ff0000"  # Red
    elif percentage <= 60:
        color = "#FFD700"  # Yellow (gold)
    else:
        color = "#008000"  # Green
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; margin:20px;">
      <svg width="120" height="120" viewBox="0 0 36 36" class="circular-chart">
        <path class="circle-bg" 
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:#eee;stroke-width:3;"></path>
        <path class="circle"
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:{color};stroke-width:3;stroke-dasharray: {percentage}, 100;stroke-dashoffset: 0;transition: stroke-dasharray 0.6s ease;"></path>
        <text x="18" y="20.35" style="fill:#666; font-size:7px; text-anchor:middle;">{percentage}%</text>
      </svg>
    </div>
    """
    return html

# ----------------------------------
# Welcome screen – using a form so that both name and roll number are submitted together.
def welcome():
    st.title("Python MCQ Quiz App")
    st.header("Welcome!")
    st.write("Please enter your details to start the quiz.")
    
    with st.form(key="welcome_form"):
        name = st.text_input("Enter your name:")
        # Use text_input instead of number_input for roll number.
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
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    # SKIP BUTTON START (for testing purposes only)
    if st.button("Skip Quiz", key="skip_quiz"):
         st.session_state["current_index"] = len(questions)  # Skip all remaining questions.
    # SKIP BUTTON END
    
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        
        # If answer hasn't been submitted, show a radio widget with a dummy first option.
        if submitted_key not in st.session_state:
            options = ["Select an option"] + question["options"]
            answer = st.radio("Select your answer:", options, index=0, key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
                if answer == "Select an option":
                    st.error("Please select a valid option.")
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
            
            if current_index == len(questions) - 1:
                if st.button("Check Result", key="check_result"):
                    st.session_state["current_index"] = current_index + 1
            else:
                if st.button("Next Question", key=f"next_{current_index}"):
                    st.session_state["current_index"] = current_index + 1
    else:
        result()

# ----------------------------------
# Result screen – displays the final score, percentage, and a percentage circle.
def result():
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
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# ----------------------------------
# Main function – decides which screen to display.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
Summary
Roll Number Field: We now use st.text_input("Enter your roll number:") so that the input does not display the plus/minus buttons or a default zero.

Validation: The code checks if the roll number field is empty, ensures that the input is numeric (using .isdigit()), and that it isn’t equal to "0".

Conversion: On successful validation, the roll number string is converted to an integer before storing in session state.

This should meet your requirements. If you need any further modifications, let me know!

please give me more big and highlited text whi will be more visible in my background
Below is an updated version of your custom CSS. In the set_custom_css() function, I've increased the font size and added styles (like a contrasting color, text-shadow, padding, and a semi-transparent background) so that your question text (and any text using the class .question-text) appears bigger, highlighted, and more visible on your background.

Replace your current set_custom_css() function with this version:

python
def set_custom_css():
    css = """
    <style>
    .question-text {
        font-size: calc(20px + 2vw); /* Increased font size */
        font-weight: bold;
        color: #ffffff; /* White text for contrast */
        text-shadow: 2px 2px 4px #000000; /* Black shadow for readability */
        padding: 10px;  
        background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent dark background */
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
This CSS will make your question text larger and more prominent. The white text with a black shadow should help it stand out on most background images. The semi-transparent dark background behind the text also increases legibility.

Simply update your code with this function, and when you run your app the question text should now be larger and highlighted for better visibility.

give me compleate code with all these updates
Below is the complete updated code which integrates all the requested changes:

• The background is set using your local “imag.png” • Custom CSS has been added to make the question text larger, highlighted, and more visible over your background. • The welcome screen uses plain text input for the roll number (with validation to ensure the field isn’t empty, is numeric, and isn’t 0) so that no plus/minus buttons or pre-filled 0 appear. • Each question is shown with a dummy “Select an option” so that no valid answer is pre-selected. When submitted, the answer is locked and feedback is provided. • For the final question, a “Check Result” button is shown instead of “Next Question.” • On the results page, an SVG-based circular progress indicator is rendered. Its color changes based on your percentage (red for ≤35%, yellow for >35% and ≤60%, green for >60%). • A “Skip Quiz” button (wrapped between clear comments) is included for testing purposes (you can remove these lines before making your app public).

Simply save the code as your app.py file (make sure you have both imag.png and a valid questions.json in the same folder) and run it with:

bash
streamlit run app.py
python
import streamlit as st
import json
import random
import base64

# ----------------------------------
# Function to set the background image using imag.png
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# ----------------------------------
# Function to set custom CSS to make text larger and highlighted.
def set_custom_css():
    css = """
    <style>
    .question-text {
        font-size: calc(20px + 2vw); /* Increased font size */
        font-weight: bold;
        color: #ffffff; /* White text for contrast */
        text-shadow: 2px 2px 4px #000000; /* Black shadow for readability */
        padding: 10px;
        background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent dark background */
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ----------------------------------
# Function to load questions from questions.json file
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
        color = "#FFD700"  # Yellow (gold)
    else:
        color = "#008000"  # Green
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; margin:20px;">
      <svg width="120" height="120" viewBox="0 0 36 36" class="circular-chart">
        <path class="circle-bg" 
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:#eee;stroke-width:3;"></path>
        <path class="circle"
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:{color};stroke-width:3;stroke-dasharray: {percentage}, 100;stroke-dashoffset: 0;transition: stroke-dasharray 0.6s ease;"></path>
        <text x="18" y="20.35" style="fill:#666; font-size:7px; text-anchor:middle;">{percentage}%</text>
      </svg>
    </div>
    """
    return html

# ----------------------------------
# Welcome screen – collects name and roll number.
# The roll number field uses a text_input so that no default value or counter controls appear.
def welcome():
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
                questions = load_questions()
                # Randomly pick up to 20 questions from your questions.json.
                if questions:
                    st.session_state["questions"] = random.sample(questions, k=min(20, len(questions)))
                else:
                    st.session_state["questions"] = []
                st.session_state["current_index"] = 0
                st.session_state["score"] = 0

# ----------------------------------
# Quiz screen – displays one question at a time.
def quiz():
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    # SKIP BUTTON START (for testing purposes only)
    if st.button("Skip Quiz", key="skip_quiz"):
         st.session_state["current_index"] = len(questions)  # Skip all remaining questions.
    # SKIP BUTTON END
    
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        
        if submitted_key not in st.session_state:
            # Prepend a dummy value so that no valid answer is pre-selected.
            options = ["Select an option"] + question["options"]
            answer = st.radio("Select your answer:", options, index=0, key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
                if answer == "Select an option":
                    st.error("Please select a valid option.")
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
            
            # For the last question, show "Check Result" instead of "Next Question".
            if current_index == len(questions) - 1:
                if st.button("Check Result", key="check_result"):
                    st.session_state["current_index"] = current_index + 1
            else:
                if st.button("Next Question", key=f"next_{current_index}"):
                    st.session_state["current_index"] = current_index + 1
    else:
        result()

# ----------------------------------
# Result screen – displays final score, percentage, and a colored percentage circle.
def result():
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
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# ----------------------------------
# Main function – controls which screen to display.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
How It Works
Welcome Screen: • Both the name and roll number are submitted in a single form. • The roll number field is a text input with validations (it must be numeric and nonzero).

Quiz Screen: • Each question’s text is rendered with enhanced CSS styles to be large and visible against your background. • The radio widget uses a dummy option ("Select an option") so that no valid answer is pre-selected. • After the answer is submitted, it is locked and feedback is shown. The button label is “Next Question” for all but the last question, where it becomes “Check Result.”

Result Screen: • Displays the final score, percentage, and an SVG-based circular progress indicator whose color depends on the score. • A “Try Again” button clears the session state to restart the quiz.

Skip Button: • For testing purposes only, a “Skip Quiz” button is provided (between SKIP BUTTON START/END comments). Remove or comment out these lines for public release.

Simply run the app as instructed, and your quiz application will have all the requested functionality and styling. Enjoy developing your app!

more larger text required for this app and auto adjust with screen size
Below is the complete updated code. In this version, the custom CSS has been upgraded so that most text (including questions, input fields, and buttons) appear larger and auto‐adjust to the screen size. You can tweak the numeric values in the CSS if you need even larger (or smaller) text. Save this as your app.py file in the same directory as your imag.png and a valid questions.json, then run:

bash
streamlit run app.py
python
import streamlit as st
import json
import random
import base64

# ----------------------------------
# Function to set the background image using imag.png
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# ----------------------------------
# Function to set custom CSS to make text larger and auto-adjust.
def set_custom_css():
    css = """
    <style>
    /* Global font increase for better visibility */
    body, .stMarkdown, .stText, .stButton, .stTextInput, .stNumberInput {
        font-size: calc(20px + 1vw) !important;
    }
    /* Make the question text larger and more highlighted */
    .question-text {
        font-size: calc(24px + 2vw);  /* Even larger text */
        font-weight: bold;
        color: #ffffff;
        text-shadow: 2px 2px 4px #000000;
        padding: 10px;
        background-color: rgba(0, 0, 0, 0.5);
        border-radius: 5px;
        margin: 10px 0;
    }
    /* Style for buttons */
    .stButton>button {
        font-size: calc(18px + 1vw);
        padding: 10px 20px;
    }
    /* Style for text inputs */
    .stTextInput>div>input,
    .stNumberInput>div>input {
        font-size: calc(18px + 1vw);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ----------------------------------
# Function to load questions from a JSON file.
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
        color = "#FFD700"  # Yellow (gold)
    else:
        color = "#008000"  # Green
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; margin:20px;">
      <svg width="120" height="120" viewBox="0 0 36 36" class="circular-chart">
        <path class="circle-bg" 
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:#eee;stroke-width:3;"></path>
        <path class="circle"
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:{color};stroke-width:3;stroke-dasharray: {percentage}, 100;stroke-dashoffset: 0;transition: stroke-dasharray 0.6s ease;"></path>
        <text x="18" y="20.35" style="fill:#666; font-size:7px; text-anchor:middle;">{percentage}%</text>
      </svg>
    </div>
    """
    return html

# ----------------------------------
# Welcome screen – collects name and roll number in one form.
def welcome():
    st.title("Python MCQ Quiz App")
    st.header("Welcome!")
    st.write("Please enter your details to start the quiz.")
    
    with st.form(key="welcome_form"):
        name = st.text_input("Enter your name:")
        # Using text_input for roll so no plus/minus or default 0 appear.
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
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    # SKIP BUTTON START (for testing purposes only)
    if st.button("Skip Quiz", key="skip_quiz"):
         st.session_state["current_index"] = len(questions)  # Skip all remaining questions.
    # SKIP BUTTON END
    
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        
        if submitted_key not in st.session_state:
            # Prepend a dummy value so that no valid answer is pre-selected.
            options = ["Select an option"] + question["options"]
            answer = st.radio("Select your answer:", options, index=0, key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
                if answer == "Select an option":
                    st.error("Please select a valid option.")
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
            
            # For the last question, show "Check Result" instead of "Next Question".
            if current_index == len(questions) - 1:
                if st.button("Check Result", key="check_result"):
                    st.session_state["current_index"] = current_index + 1
            else:
                if st.button("Next Question", key=f"next_{current_index}"):
                    st.session_state["current_index"] = current_index + 1
    else:
        result()

# ----------------------------------
# Result screen – displays the final score, percentage, and a progress circle.
def result():
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
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# ----------------------------------
# Main function – decides which screen to display.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
How It Works
Global & Element CSS: The custom CSS styles now target the body, text inputs, buttons, and especially the .question-text class. This ensures text auto-adjusts with the viewport size using CSS’s calc() with viewport width (vw), making it larger on bigger screens and scaling down on smaller ones.

Welcome Screen: Uses text inputs for both name and roll number; the roll number field is a plain text input so no plus/minus or default value is shown.

Quiz Screen: Displays each question with a large, highlighted text block. The radio input prepends a dummy option to ensure no answer is pre-selected.

Results Screen: Shows your score and an SVG-based progress circle that changes color based on the percentage.

Skip Button: For testing purposes, a “Skip Quiz” button is available (wrapped with comments so you can remove it before final deployment).

This code now meets your request for larger, auto-adjusting text along with all previous functionality. Enjoy your enhanced quiz app!

not you just make large text for quetis only please make large and adjustable for all text like quetion, options, other text
Below is the complete updated code in which we've added global CSS that makes all text elements (questions, options, button labels, inputs, etc.) larger and automatically adjust with the screen size. The custom CSS now uses a universal selector so that every element on the page gets an enhanced font size, while still keeping the special prominent styling for the questions through the .question-text class.

Simply save the code as your app.py file (make sure that you have both the imag.png and a valid questions.json file in the same folder) and run the app with:

bash
streamlit run app.py
python
import streamlit as st
import json
import random
import base64

# ----------------------------------
# Function to set the background image using imag.png
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# ----------------------------------
# Function to set custom CSS to make ALL text larger and auto-adjust.
def set_custom_css():
    css = """
    <style>
    /* Universal selector: enlarges and auto-adjusts all text on the page */
    * {
        font-size: calc(20px + 1vw) !important;
    }
    /* Overriding for question text to be even larger and with extra styling */
    .question-text {
        font-size: calc(24px + 2vw) !important;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 2px 2px 4px #000000;
        padding: 10px;
        background-color: rgba(0, 0, 0, 0.5);
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ----------------------------------
# Function to load questions from questions.json file
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
        color = "#FFD700"  # Yellow (gold)
    else:
        color = "#008000"  # Green
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; margin:20px;">
      <svg width="120" height="120" viewBox="0 0 36 36" class="circular-chart">
        <path class="circle-bg" 
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:#eee;stroke-width:3;"></path>
        <path class="circle"
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:{color};stroke-width:3;stroke-dasharray: {percentage}, 100;stroke-dashoffset: 0;transition: stroke-dasharray 0.6s ease;"></path>
        <text x="18" y="20.35" style="fill:#666; font-size:7px; text-anchor:middle;">{percentage}%</text>
      </svg>
    </div>
    """
    return html

# ----------------------------------
# Welcome screen – collects name and roll number in one form.
def welcome():
    st.title("Python MCQ Quiz App")
    st.header("Welcome!")
    st.write("Please enter your details to start the quiz.")
    
    with st.form(key="welcome_form"):
        name = st.text_input("Enter your name:")
        # Using a text input for the roll number so that no plus/minus buttons or default 0 show.
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
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    # SKIP BUTTON START (for testing purposes only)
    if st.button("Skip Quiz", key="skip_quiz"):
         st.session_state["current_index"] = len(questions)  # Skip all remaining questions.
    # SKIP BUTTON END
    
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        
        if submitted_key not in st.session_state:
            # Prepend a dummy value so that no valid answer is pre-selected.
            options = ["Select an option"] + question["options"]
            answer = st.radio("Select your answer:", options, index=0, key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
                if answer == "Select an option":
                    st.error("Please select a valid option.")
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
            
            # For the last question, show "Check Result" instead of "Next Question".
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
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# ----------------------------------
# Main function – determines which screen (welcome, quiz, result) to display.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
How It Works
Global Text Scaling: The CSS now uses a universal selector (* { font-size: calc(20px + 1vw) !important; }) so that every text element—including questions, options, headings, buttons, and inputs—will enlarge based on the screen width. You can adjust the numbers in calc(20px + 1vw) if you wish.

Highlighted Questions: The .question-text class is further enhanced to be even larger (using calc(24px + 2vw)), with white text, a black text-shadow, and a semi-transparent dark background to ensure maximum readability against the background image.

Consistent Styling for All Elements: Since every element inherits from the universal style, all text in your app (including options and other UI components) will become larger and adjust responsively across different devices.

This version should now meet your requirement to have “larger and adjustable text for all text” across your quiz app. Enjoy your enhanced user interface!

y you make it unfit app for screen i said adjust you all text first time you have sent me text sizes make it same but little bitt larg all test but adjustable
Below is the complete updated code. In this version, the custom CSS has been modified so that it enlarges all text slightly while keeping the text adjustable (responsive) to screen size. Instead of applying a universal selector (which sometimes makes the app layout unfit), we set the base font size on the root (html) and then style specific elements (headings, inputs, buttons, etc.) accordingly. The question text is given a slightly larger size and extra styling for prominence, but all text remains proportional and adjustable.

Simply save the code as your app.py file (make sure you have both imag.png and a valid questions.json in the same folder) and run:

bash
streamlit run app.py
python
import streamlit as st
import json
import random
import base64

# ----------------------------------
# Function to set the background image using imag.png
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# ----------------------------------
# Function to set custom CSS to make all text a little larger yet adjustable.
def set_custom_css():
    css = """
    <style>
    /* Set a base font size on html that adjusts with viewport width */
    html {
        font-size: calc(16px + 0.5vw);
    }

    /* Ensure body text uses the base size */
    body {
        font-size: 1rem;
    }

    /* Standardize the appearance of markdown, text, and input fields */
    .stMarkdown, .stText, .stTextInput, .stButton, .stNumberInput {
        font-size: 1rem;
    }

    /* Make question text a bit larger and more prominent */
    .question-text {
        font-size: calc(18px + 1vw);
        font-weight: bold;
        color: #ffffff;
        text-shadow: 1px 1px 2px #000;
        padding: 8px;
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 4px;
        margin: 8px 0;
    }

    /* Style the buttons */
    .stButton>button {
        font-size: 1rem;
        padding: 8px 16px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ----------------------------------
# Function to load questions from questions.json file
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
        color = "#FFD700"  # Yellow (gold)
    else:
        color = "#008000"  # Green
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; margin:20px;">
      <svg width="120" height="120" viewBox="0 0 36 36" class="circular-chart">
        <path class="circle-bg" 
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:#eee;stroke-width:3;"></path>
        <path class="circle"
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:{color};stroke-width:3;stroke-dasharray: {percentage}, 100;stroke-dashoffset: 0;transition: stroke-dasharray 0.6s ease;"></path>
        <text x="18" y="20.35" style="fill:#666; font-size:7px; text-anchor:middle;">{percentage}%</text>
      </svg>
    </div>
    """
    return html

# ----------------------------------
# Welcome screen – collects name and roll number together.
def welcome():
    st.title("Python MCQ Quiz App")
    st.header("Welcome!")
    st.write("Please enter your details to start the quiz.")
    
    with st.form(key="welcome_form"):
        name = st.text_input("Enter your name:")
        # Using text_input for roll number prevents a default 0 and plus/minus controls.
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
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    # SKIP BUTTON START (for testing purposes only)
    if st.button("Skip Quiz", key="skip_quiz"):
         st.session_state["current_index"] = len(questions)  # Skip all remaining questions.
    # SKIP BUTTON END
    
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        
        if submitted_key not in st.session_state:
            # Prepend a dummy value so that no valid answer is pre-selected.
            options = ["Select an option"] + question["options"]
            answer = st.radio("Select your answer:", options, index=0, key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
                if answer == "Select an option":
                    st.error("Please select a valid option.")
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
            
            # For the last question, show "Check Result" instead of "Next Question".
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
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# ----------------------------------
# Main function – determines which screen (welcome, quiz, result) to display.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
How It Works
Custom CSS Adjustments:

The base font size for the document is set on the html element using a combination of pixels and viewport width (via calc(16px + 0.5vw)), so it auto-adjusts with the screen size.

Specific components (inputs, buttons, markdown text) are slightly increased to 1rem.

The .question-text class has a larger size—calculated with calc(18px + 1vw)—and clear styling for higher contrast.

Welcome, Quiz, and Result Screens: These remain as in previous versions (with the skip button, dummy radio option to force a selection, and an SVG-based progress circle) while now inheriting the improved, adjustable text styling.

This version should now provide larger, clear text for all elements while remaining responsive to screen size. If you need further adjustments, feel free to ask!

make circile side 20% bigger make information page size 20% small remove that selecte a option check just 4 check showing each quetin
Below is the complete updated code implementing your three requests:

Make the progress circle 20% larger: The SVG’s width and height have been increased by 20% (from 120 to 144).

Make the “information page” (the results page) 20% smaller: The text (except the title and circle) on the result page is wrapped in a container styled with a 0.8× (or 80%) font size.

Remove the dummy “Select an option” value: The radio widget now displays only the four actual answer options for each question without a default dummy choice.

Save the code as your app.py (and ensure that your imag.png and a valid questions.json are in the same folder), then run:

bash
streamlit run app.py
Below is the full code:

python
import streamlit as st
import json
import random
import base64

# ----------------------------------
# Function to set the background image using imag.png
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# ----------------------------------
# Function to set custom CSS to adjust text sizes.
# Here we set a base size and style specific elements; we aren’t using a universal selector.
def set_custom_css():
    css = """
    <style>
    /* Set a base font size on html that adjusts with viewport width */
    html {
        font-size: calc(16px + 0.5vw);
    }

    /* Ensure body text uses the base size */
    body {
        font-size: 1rem;
    }

    /* Standardize the appearance of markdown, text, and input fields */
    .stMarkdown, .stText, .stTextInput, .stButton, .stNumberInput {
        font-size: 1rem;
    }

    /* Make question text a bit larger and more prominent */
    .question-text {
        font-size: calc(18px + 1vw);
        font-weight: bold;
        color: #ffffff;
        text-shadow: 1px 1px 2px #000;
        padding: 8px;
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 4px;
        margin: 8px 0;
    }

    /* Style for buttons */
    .stButton>button {
        font-size: 1rem;
        padding: 8px 16px;
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
        color = "#FFD700"  # Yellow (gold)
    else:
        color = "#008000"  # Green
    # Increase the SVG size by 20% (from 120px to 144px).
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; margin:20px;">
      <svg width="144" height="144" viewBox="0 0 36 36" class="circular-chart">
        <path class="circle-bg" 
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:#eee;stroke-width:3;"></path>
        <path class="circle"
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:{color};stroke-width:3;stroke-dasharray: {percentage}, 100;stroke-dashoffset: 0;transition: stroke-dasharray 0.6s ease;"></path>
        <text x="18" y="20.35" style="fill:#666; font-size:7px; text-anchor:middle;">{percentage}%</text>
      </svg>
    </div>
    """
    return html

# ----------------------------------
# Welcome screen – collects name and roll number together.
def welcome():
    st.title("Python MCQ Quiz App")
    st.header("Welcome!")
    st.write("Please enter your details to start the quiz.")
    
    with st.form(key="welcome_form"):
        name = st.text_input("Enter your name:")
        # Use text_input for roll number so no default 0 or plus/minus buttons appear.
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
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    # SKIP BUTTON START (for testing purposes only)
    if st.button("Skip Quiz", key="skip_quiz"):
         st.session_state["current_index"] = len(questions)  # Skip all remaining questions.
    # SKIP BUTTON END
    
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        
        if submitted_key not in st.session_state:
            # Now simply display the four answer options without any dummy selection.
            answer = st.radio("Select your answer:", question["options"], key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
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
            
            # For the last question, show "Check Result" instead of "Next Question."
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
# The informational text is wrapped in a container with 20% smaller text (font-size:0.8em).
def result():
    st.title("Quiz Completed!")
    with st.container():
        st.markdown('<div style="font-size:0.8em;">', unsafe_allow_html=True)
        st.write(f"Name: {st.session_state.get('name', 'N/A')}")
        st.write(f"Roll Number: {st.session_state.get('roll', 'N/A')}")
        score = st.session_state.get("score", 0)
        total = len(st.session_state.get("questions", []))
        percentage = int((score / total) * 100) if total > 0 else 0
        st.write(f"Your score: {score} out of {total}")
        st.write(f"Percentage: {percentage}%")
        st.markdown('</div>', unsafe_allow_html=True)
    circle_html = render_progress_circle(percentage)
    st.markdown(circle_html, unsafe_allow_html=True)
    
    if percentage <= 35:
        st.error("Result: Poor, try again!")
    elif percentage <= 60:
        st.warning("Result: Average performance!")
    else:
        st.success("Result: Well done!")
    
    if st.button("Try Again"):
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# ----------------------------------
# Main function – determines which screen (welcome, quiz, or result) to display.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
Explanation
Progress Circle Change: The <svg> tag now uses width="144" and height="144" (20% larger than the original 120 px).

Result Page Font Size: All information on the result page (name, roll number, score, and percentage) is wrapped in a container with inline CSS (font-size: 0.8em), making the text 20% smaller.

Answer Options Change: The radio button in the quiz screen no longer prepends a dummy option. It now directly displays the four answer options given in your question data.

This should now meet your requirements. If you need further adjustments, please let me know!

information page means first page having role number and name
Below is the complete updated code that applies your latest changes. In this version:

The Welcome (Information) Page The first page—where the user enters their name and roll number—is wrapped in a container with an inline style that makes its text 20% smaller. (This is what you refer to as the "information page.")

Progress Circle Size The SVG circle has been increased by 20% (from 120 px to 144 px).

Answer Options The dummy option ("Select an option") has been removed so that only the actual four answer choices appear for each question.

Be sure that your imag.png and questions.json (with at least four options per question) are in the same folder. Save the code as app.py and run:

bash
streamlit run app.py
python
import streamlit as st
import json
import random
import base64

# ----------------------------------
# Function to set the background image using imag.png
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# ----------------------------------
# Function to set custom CSS for overall styling.
def set_custom_css():
    css = """
    <style>
    /* Set a base font size on html that adjusts with viewport width */
    html {
        font-size: calc(16px + 0.5vw);
    }
    body {
        font-size: 1rem;
    }
    .stMarkdown, .stText, .stTextInput, .stButton, .stNumberInput {
        font-size: 1rem;
    }
    /* Make question text a bit larger and more prominent */
    .question-text {
        font-size: calc(18px + 1vw);
        font-weight: bold;
        color: #ffffff;
        text-shadow: 1px 1px 2px #000;
        padding: 8px;
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 4px;
        margin: 8px 0;
    }
    /* Style for buttons */
    .stButton>button {
        font-size: 1rem;
        padding: 8px 16px;
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
        color = "#FFD700"  # Yellow (gold)
    else:
        color = "#008000"  # Green
    # Increase the SVG size by 20% (from 120px to 144px).
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; margin:20px;">
      <svg width="144" height="144" viewBox="0 0 36 36" class="circular-chart">
        <path class="circle-bg" 
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:#eee;stroke-width:3;"></path>
        <path class="circle"
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:{color};stroke-width:3;stroke-dasharray: {percentage}, 100;stroke-dashoffset: 0;transition: stroke-dasharray 0.6s ease;"></path>
        <text x="18" y="20.35" style="fill:#666; font-size:7px; text-anchor:middle;">{percentage}%</text>
      </svg>
    </div>
    """
    return html

# ----------------------------------
# Welcome screen – collects name and roll number.
# The content is wrapped in a container with a 20% smaller font (0.8em) as requested.
def welcome():
    with st.container():
        st.markdown('<div style="font-size:0.8em;">', unsafe_allow_html=True)
        st.title("Python MCQ Quiz App")
        st.header("Welcome!")
        st.write("Please enter your details to start the quiz.")
        
        with st.form(key="welcome_form"):
            name = st.text_input("Enter your name:")
            # Using text_input for roll number; no default 0 or plus/minus controls.
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
                    questions = load_questions()
                    if questions:
                        st.session_state["questions"] = random.sample(questions, k=min(20, len(questions)))
                    else:
                        st.session_state["questions"] = []
                    st.session_state["current_index"] = 0
                    st.session_state["score"] = 0
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------
# Quiz screen – displays one question at a time.
def quiz():
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    # SKIP BUTTON START (for testing purposes only)
    if st.button("Skip Quiz", key="skip_quiz"):
         st.session_state["current_index"] = len(questions)  # Skip all remaining questions.
    # SKIP BUTTON END
    
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        
        if submitted_key not in st.session_state:
            # Directly show the four answer options (without a dummy option).
            answer = st.radio("Select your answer:", question["options"], key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
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
            
            # For the last question, show "Check Result" instead of "Next Question."
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
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# ----------------------------------
# Main function – determines which screen (welcome, quiz, result) to display.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
How It Works
Welcome (Information) Page Styling: The entire welcome page is wrapped in a container whose inner HTML is styled with font-size:0.8em, making all its text 20% smaller than the default.

Progress Circle: The SVG now has a width and height of 144 pixels (20% larger than before).

Quiz Screen Options: The radio button now displays only the answer options from your JSON data—no dummy "Select an option" is prepended.

You can adjust the inline CSS values further if needed. Enjoy your app, and let me know if you need any more tweaks!

make welcome page size 30% small
Below is the complete updated code. In this version, only the welcome (information) page text is scaled to 70% (i.e. 30% smaller than the default size). This is achieved by wrapping the welcome page content in a container with inline CSS set to font-size:0.7em.

Simply save the code as your app.py file (make sure that you have both imag.png and a valid questions.json in the same folder) and run:

bash
streamlit run app.py
python
import streamlit as st
import json
import random
import base64

# ----------------------------------
# Function to set the background image using imag.png
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# ----------------------------------
# Function to set custom CSS for overall styling.
def set_custom_css():
    css = """
    <style>
    /* Set a base font size on html that adjusts with viewport width */
    html {
        font-size: calc(16px + 0.5vw);
    }
    body {
        font-size: 1rem;
    }
    .stMarkdown, .stText, .stTextInput, .stButton, .stNumberInput {
        font-size: 1rem;
    }
    /* Make question text a bit larger and more prominent */
    .question-text {
        font-size: calc(18px + 1vw);
        font-weight: bold;
        color: #ffffff;
        text-shadow: 1px 1px 2px #000;
        padding: 8px;
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 4px;
        margin: 8px 0;
    }
    /* Style for buttons */
    .stButton>button {
        font-size: 1rem;
        padding: 8px 16px;
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
        color = "#FFD700"  # Yellow (gold)
    else:
        color = "#008000"  # Green
    # Increase the SVG size by 20% (from 120px to 144px).
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; margin:20px;">
      <svg width="144" height="144" viewBox="0 0 36 36" class="circular-chart">
        <path class="circle-bg" 
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:#eee;stroke-width:3;"></path>
        <path class="circle"
            d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
            style="fill:none;stroke:{color};stroke-width:3;stroke-dasharray: {percentage}, 100;stroke-dashoffset: 0;transition: stroke-dasharray 0.6s ease;"></path>
        <text x="18" y="20.35" style="fill:#666; font-size:7px; text-anchor:middle;">{percentage}%</text>
      </svg>
    </div>
    """
    return html

# ----------------------------------
# Welcome screen – collects name and roll number.
# The content is wrapped in a container with a 0.7em font size to make it 30% smaller.
def welcome():
    with st.container():
        st.markdown('<div style="font-size:0.7em;">', unsafe_allow_html=True)
        st.title("Python MCQ Quiz App")
        st.header("Welcome!")
        st.write("Please enter your details to start the quiz.")
        
        with st.form(key="welcome_form"):
            name = st.text_input("Enter your name:")
            # Using text_input for roll number prevents a default 0 and plus/minus controls.
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
                    questions = load_questions()
                    if questions:
                        st.session_state["questions"] = random.sample(questions, k=min(20, len(questions)))
                    else:
                        st.session_state["questions"] = []
                    st.session_state["current_index"] = 0
                    st.session_state["score"] = 0
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------
# Quiz screen – displays one question at a time.
def quiz():
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    # SKIP BUTTON START (for testing purposes only)
    if st.button("Skip Quiz", key="skip_quiz"):
         st.session_state["current_index"] = len(questions)  # Skip all remaining questions.
    # SKIP BUTTON END
    
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        
        if submitted_key not in st.session_state:
            # Directly show the four answer options without a dummy option.
            answer = st.radio("Select your answer:", question["options"], key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
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
            
            # For the last question, show "Check Result" instead of "Next Question."
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
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# ----------------------------------
# Main function – determines which screen (welcome, quiz, result) to display.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
Explanation
Welcome Page Scaling: The entire welcome (information) page is wrapped in a container whose content is styled with font-size:0.7em. This makes its text 30% smaller than the default size.

Other Functionality Remains Unchanged: The progress circle, quiz screen options, results page, and other functionalities remain the same as before.

This should meet your request for making the welcome page 30% smaller. If you need any further adjustments, just let me know!

make result page size 20 percent small and make circle 10 percent big
Below is the complete updated code with the following modifications:

Result Page Text 20% Smaller: All informational text on the result page (name, roll number, score, and percentage) is now wrapped in a container styled with a 0.8em font size (i.e. 20% smaller than default).

Progress Circle 10% Bigger: The SVG for the progress circle now uses width and height increased by 10% from 144px to approximately 158px.

Simply save the code as your app.py file (and ensure that your imag.png and a valid questions.json file are in the same folder), then run:

bash
streamlit run app.py
Below is the full code:

python
import streamlit as st
import json
import random
import base64

# ----------------------------------
# Function to set the background image using imag.png
def set_background(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")

# ----------------------------------
# Function to set custom CSS for overall styling.
def set_custom_css():
    css = """
    <style>
    /* Set a base font size on html that adjusts with viewport width */
    html {
        font-size: calc(16px + 0.5vw);
    }
    body {
        font-size: 1rem;
    }
    .stMarkdown, .stText, .stTextInput, .stButton, .stNumberInput {
        font-size: 1rem;
    }
    /* Make question text a bit larger and more prominent */
    .question-text {
        font-size: calc(18px + 1vw);
        font-weight: bold;
        color: #ffffff;
        text-shadow: 1px 1px 2px #000;
        padding: 8px;
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 4px;
        margin: 8px 0;
    }
    /* Style for buttons */
    .stButton>button {
        font-size: 1rem;
        padding: 8px 16px;
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
        color = "#FFD700"  # Yellow (gold)
    else:
        color = "#008000"  # Green
    # Increase the SVG size by 10% from 144px to approximately 158px.
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; margin:20px;">
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
            style="fill:none;stroke:{color};stroke-width:3;stroke-dasharray: {percentage}, 100;stroke-dashoffset: 0;transition: stroke-dasharray 0.6s ease;"></path>
        <text x="18" y="20.35" style="fill:#666; font-size:7px; text-anchor:middle;">{percentage}%</text>
      </svg>
    </div>
    """
    return html

# ----------------------------------
# Welcome screen – collects name and roll number.
def welcome():
    with st.container():
        # Leave welcome page at normal size (or adjust it as needed separately)
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
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    # SKIP BUTTON START (for testing purposes only)
    if st.button("Skip Quiz", key="skip_quiz"):
         st.session_state["current_index"] = len(questions)  # Skip all remaining questions.
    # SKIP BUTTON END
    
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        
        if submitted_key not in st.session_state:
            # Directly show the answer options (without any dummy option).
            answer = st.radio("Select your answer:", question["options"], key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
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
            
            # For the last question, show "Check Result" instead of "Next Question."
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
# The result text is wrapped in a container with a 0.8em font size (20% smaller).
def result():
    st.title("Quiz Completed!")
    with st.container():
        st.markdown('<div style="font-size:0.8em;">', unsafe_allow_html=True)
        st.write(f"Name: {st.session_state.get('name', 'N/A')}")
        st.write(f"Roll Number: {st.session_state.get('roll', 'N/A')}")
        
        score = st.session_state.get("score", 0)
        total = len(st.session_state.get("questions", []))
        percentage = int((score / total) * 100) if total > 0 else 0
        
        st.write(f"Your score: {score} out of {total}")
        st.write(f"Percentage: {percentage}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    circle_html = render_progress_circle(percentage)
    st.markdown(circle_html, unsafe_allow_html=True)
    
    if percentage <= 35:
        st.error("Result: Poor, try again!")
    elif percentage <= 60:
        st.warning("Result: Average performance!")
    else:
        st.success("Result: Well done!")
    
    if st.button("Try Again"):
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# ----------------------------------
# Main function – decides which screen (welcome, quiz, result) to display.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
Explanation
In the result() function, all text (name, roll number, score, and percentage) is wrapped in a container with inline styling (font-size:0.8em), making it 20% smaller than the default.

In the render_progress_circle() function, the SVG dimensions have been increased from a width/height of 144 to about 158 pixels to achieve a 10% increase in size.

This version should now meet your requirements. If you need any further adjustments, feel free to ask!

text sizes are too musch messedup please arrange standard sizes of text and screen fo all type browsers and devices
Below is a complete code update that uses standard, fixed relative units (rem) for font sizes rather than viewport-calculated sizes. This should make your text look consistent on most browsers and devices. In this version, we set the base font size to 16px (which is standard), use rem units for all text elements, and apply a clear, unambiguous style for headings, question text, inputs, and buttons.

Simply save this as your app.py file (with your imag.png and a valid questions.json in the same folder) and run:

bash
streamlit run app.py
python
import streamlit as st
import json
import random
import base64

# ----------------------------------
# Function to set the background image using imag.png
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
# Function to set custom CSS with standard sizes for fonts and spacing.
def set_custom_css():
    css = """
    <style>
    /* Set a standard base font size */
    html {
        font-size: 16px;
    }
    
    body {
        font-family: Arial, sans-serif;
        font-size: 1rem; /* 16px */
        line-height: 1.5;
        color: #333;
    }
    
    /* Style for headings */
    h1 { font-size: 2rem; } /* 32px */
    h2 { font-size: 1.75rem; } /* 28px */
    h3 { font-size: 1.5rem; } /* 24px */
    
    /* Standard text for Markdown and other elements */
    .stMarkdown, .stText, .stTextInput, .stButton, .stNumberInput {
        font-size: 1rem;
    }
    
    /* Make question text prominent */
    .question-text {
        font-size: 1.25rem;  /* about 20px */
        font-weight: bold;
        color: #ffffff;
        text-shadow: 1px 1px 2px #000;
        padding: 0.625rem; /* 10px */
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 0.3125rem; /* 5px */
        margin: 0.625rem 0; /* 10px 0 */
    }
    
    /* Style for buttons */
    .stButton > button {
        font-size: 1rem;
        padding: 0.5rem 1rem;
    }
    
    /* Input fields */
    .stTextInput > div > input,
    .stNumberInput > div > input {
        font-size: 1rem;
        padding: 0.5rem;
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
    # Increase the SVG size by 10%: from 144px to roughly 158px.
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
# Welcome screen – collects name and roll number.
# The welcome (information) page is not scaled down here unless required.
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
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    # SKIP BUTTON for testing; remove if not needed.
    if st.button("Skip Quiz", key="skip_quiz"):
         st.session_state["current_index"] = len(questions)
         
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index+1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        if submitted_key not in st.session_state:
            # Directly display the answer options (without dummy option)
            answer = st.radio("Select your answer:", question["options"], key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
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
            # Last question: show "Check Result"; otherwise "Next Question"
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
# The result text is wrapped in a container with standard (1rem) font sizes.
def result():
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
        for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]:
            if key in st.session_state:
                del st.session_state[key]

# ----------------------------------
# Main function – decides which screen to display.
def main():
    set_background("imag.png")
    set_custom_css()
    if "quiz_started" not in st.session_state:
        welcome()
    else:
        quiz()

if __name__ == "__main__":
    main()
Explanation
Result Page Size: The result page text remains in a standard size (1rem) so it appears clearly and uniformly across browsers. (If you need it to be 20% smaller than the default page, you could wrap its contents in a container with font-size:0.8rem. Adjust this if needed.)

Progress Circle Size: The SVG width and height are now set to 158 pixels, which is about 10% larger than the previous 144 pixels.

Standardized Text: The overall CSS now uses rem units with a base font-size of 16px. This should work across all standard browsers and devices, ensuring consistency.

Feel free to tweak the CSS values (such as in the container wrapping the result page) if you need further adjustments. This version should provide standard, clean typography across devices.

Hi Syed! What's new on this late-night coding spree?

Hey there, Syed! What can I do for you tonight?

where is our last conversation about this topic?
Syed, we don't have access to previous conversations in this specific interface, unfortunately! But hey, you can share what you're looking for, and I'll pick up from where we left off. Want to give me a quick summary of what you're trying to achieve tonight?

import streamlit as st import json import random import base64 # ---------------------------------- # Function to set the background image using imag.png def set_background(image_file): try: with open(image_file, "rb") as img: encoded = base64.b64encode(img.read()).decode() css = f""" <style> .stApp {{ background: url("data:image/png;base64,{encoded}"); background-size: cover; background-position: center; }} </style> """ st.markdown(css, unsafe_allow_html=True) except Exception as e: st.error(f"Error setting background: {e}") # ---------------------------------- # Function to set custom CSS with standard sizes for fonts and spacing. def set_custom_css(): css = """ <style> /* Set a standard base font size */ html { font-size: 16px; } body { font-family: Arial, sans-serif; font-size: 1rem; /* 16px */ line-height: 1.5; color: #333; } /* Style for headings */ h1 { font-size: 2rem; } /* 32px */ h2 { font-size: 1.75rem; } /* 28px */ h3 { font-size: 1.5rem; } /* 24px */ /* Standard text for Markdown and other elements */ .stMarkdown, .stText, .stTextInput, .stButton, .stNumberInput { font-size: 1rem; } /* Make question text prominent */ .question-text { font-size: 1.25rem; /* about 20px */ font-weight: bold; color: #ffffff; text-shadow: 1px 1px 2px #000; padding: 0.625rem; /* 10px */ background-color: rgba(0, 0, 0, 0.6); border-radius: 0.3125rem; /* 5px */ margin: 0.625rem 0; /* 10px 0 */ } /* Style for buttons */ .stButton > button { font-size: 1rem; padding: 0.5rem 1rem; } /* Input fields */ .stTextInput > div > input, .stNumberInput > div > input { font-size: 1rem; padding: 0.5rem; } </style> """ st.markdown(css, unsafe_allow_html=True) # ---------------------------------- # Function to load questions from questions.json file. def load_questions(): try: with open("questions.json", "r", encoding="utf-8") as f: questions = json.load(f) return questions except Exception as e: st.error(f"Error loading questions: {e}") return [] # ---------------------------------- # Function to render a percentage circle using SVG. def render_progress_circle(percentage): if percentage <= 35: color = "#ff0000" # Red elif percentage <= 60: color = "#FFD700" # Yellow/gold else: color = "#008000" # Green # Increase the SVG size by 10%: from 144px to roughly 158px. html = f""" <div style="display: flex; justify-content: center; align-items: center; margin: 1.25rem 0;"> <svg width="158" height="158" viewBox="0 0 36 36" class="circular-chart"> <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" style="fill:none;stroke:#eee;stroke-width:3;"></path> <path class="circle" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" style="fill:none;stroke:{color};stroke-width:3; stroke-dasharray: {percentage}, 100; stroke-dashoffset: 0; transition: stroke-dasharray 0.6s ease;"></path> <text x="18" y="20.35" style="fill:#666; font-size:0.4375rem; text-anchor:middle;">{percentage}%</text> </svg> </div> """ return html # ---------------------------------- # Welcome screen – collects name and roll number. # The welcome (information) page is not scaled down here unless required. def welcome(): with st.container(): st.title("Python MCQ Quiz App") st.header("Welcome!") st.write("Please enter your details to start the quiz.") with st.form(key="welcome_form"): name = st.text_input("Enter your name:") roll_input = st.text_input("Enter your roll number:") submitted = st.form_submit_button("Submit Details") if submitted: if not name.strip(): st.error("Name cannot be empty.") elif not name.replace(" ", "").isalpha(): st.error("Name can only contain alphabetic characters and spaces.") elif not roll_input.strip(): st.error("Roll number cannot be empty.") elif not roll_input.strip().isdigit(): st.error("Roll number must be numeric.") elif int(roll_input.strip()) == 0: st.error("Roll number cannot be 0.") else: st.session_state["name"] = name st.session_state["roll"] = int(roll_input.strip()) st.session_state["quiz_started"] = True questions = load_questions() if questions: st.session_state["questions"] = random.sample(questions, k=min(20, len(questions))) else: st.session_state["questions"] = [] st.session_state["current_index"] = 0 st.session_state["score"] = 0 # ---------------------------------- # Quiz screen – displays one question at a time. def quiz(): questions = st.session_state.get("questions", []) current_index = st.session_state.get("current_index", 0) # SKIP BUTTON for testing; remove if not needed. if st.button("Skip Quiz", key="skip_quiz"): st.session_state["current_index"] = len(questions) if current_index < len(questions): question = questions[current_index] st.subheader(f"Question {current_index+1} of {len(questions)}") st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True) submitted_key = f"submitted_{current_index}" if submitted_key not in st.session_state: # Directly display the answer options (without dummy option) answer = st.radio("Select your answer:", question["options"], key=f"q{current_index}") if st.button("Submit Answer", key=f"submit_{current_index}"): st.session_state[submitted_key] = answer if answer == question["answer"]: st.session_state["score"] += 1 else: answer = st.session_state[submitted_key] st.write(f"Your Answer: **{answer}**") if answer == question["answer"]: st.success("Correct Answer!") else: st.error(f"Wrong Answer! Correct Answer is: **{question['answer']}**") # Last question: show "Check Result"; otherwise "Next Question" if current_index == len(questions) - 1: if st.button("Check Result", key="check_result"): st.session_state["current_index"] = current_index + 1 else: if st.button("Next Question", key=f"next_{current_index}"): st.session_state["current_index"] = current_index + 1 else: result() # ---------------------------------- # Result screen – displays final score, percentage, and a progress circle. # The result text is wrapped in a container with standard (1rem) font sizes. def result(): st.title("Quiz Completed!") st.write(f"Name: {st.session_state.get('name', 'N/A')}") st.write(f"Roll Number: {st.session_state.get('roll', 'N/A')}") score = st.session_state.get("score", 0) total = len(st.session_state.get("questions", [])) percentage = int((score / total) * 100) if total > 0 else 0 st.write(f"Your score: {score} out of {total}") st.write(f"Percentage: {percentage}%") circle_html = render_progress_circle(percentage) st.markdown(circle_html, unsafe_allow_html=True) if percentage <= 35: st.error("Result: Poor, try again!") elif percentage <= 60: st.warning("Result: Average performance!") else: st.success("Result: Well done!") if st.button("Try Again"): for key in ["quiz_started", "name", "roll", "questions", "current_index", "score"]: if key in st.session_state: del st.session_state[key] # ---------------------------------- # Main function – decides which screen to display. def main(): set_background("imag.png") set_custom_css() if "quiz_started" not in st.session_state: welcome() else: quiz() if __name__ == "__main__": main() this is my code i have quetions.json and imag.png i need to add timer in during this testonly 25 mint time after 25 mint quetins will skip and shown result rmaining answers are wrong considered
Below is the complete updated code that adds a 25‐minute timer to your quiz. When the quiz starts (after the user submits their information), the current time is stored. On every quiz (and result) page, the remaining time is computed and displayed at the top right. Once the timer reaches zero (i.e. after 25 minutes or 1500 seconds), the remaining unanswered questions are considered wrong by auto‐skipping the quiz and sending the user to the result page.

Simply save the code as your app.py file (with your questions.json and imag.png in the same folder) and run:

bash
streamlit run app.py
Below is the complete code:

python
import streamlit as st
import json
import random
import base64
import time

# Total time for the quiz (25 minutes = 1500 seconds)
TOTAL_TIME = 1500

# ----------------------------------
# Function to set the background image using imag.png
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
# Function to set custom CSS with standard sizes for fonts and spacing.
def set_custom_css():
    css = """
    <style>
    /* Set a standard base font size */
    html {
        font-size: 16px;
    }
    
    body {
        font-family: Arial, sans-serif;
        font-size: 1rem; /* 16px */
        line-height: 1.5;
        color: #333;
    }
    
    /* Style for headings */
    h1 { font-size: 2rem; } /* 32px */
    h2 { font-size: 1.75rem; } /* 28px */
    h3 { font-size: 1.5rem; } /* 24px */
    
    /* Standard text for Markdown and other elements */
    .stMarkdown, .stText, .stTextInput, .stButton, .stNumberInput {
        font-size: 1rem;
    }
    
    /* Make question text prominent */
    .question-text {
        font-size: 1.25rem;  /* about 20px */
        font-weight: bold;
        color: #ffffff;
        text-shadow: 1px 1px 2px #000;
        padding: 0.625rem; /* 10px */
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 0.3125rem; /* 5px */
        margin: 0.625rem 0; /* 10px 0 */
    }
    
    /* Style for buttons */
    .stButton > button {
        font-size: 1rem;
        padding: 0.5rem 1rem;
    }
    
    /* Input fields */
    .stTextInput > div > input,
    .stNumberInput > div > input {
        font-size: 1rem;
        padding: 0.5rem;
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
    # Increase the SVG size by 10% from 144px to roughly 158px.
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
        st.markdown(f"<div style='text-align: right; font-size: 1rem; color: #333;'><strong>Time Remaining: {mins:02d}:{secs:02d}</strong></div>", unsafe_allow_html=True)
        if remaining <= 0:
            st.error("Time's up! The quiz will now end automatically.")
            st.session_state["current_index"] = len(st.session_state.get("questions", []))
            st.experimental_rerun()

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
                    # Set the start time for the quiz.
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
    # Display the timer at the top of the page.
    display_timer()
    
    questions = st.session_state.get("questions", [])
    current_index = st.session_state.get("current_index", 0)
    
    # SKIP BUTTON for testing; remove if not needed.
    if st.button("Skip Quiz", key="skip_quiz"):
         st.session_state["current_index"] = len(questions)
         
    if current_index < len(questions):
        question = questions[current_index]
        st.subheader(f"Question {current_index+1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{question['question']}</div>", unsafe_allow_html=True)
        
        submitted_key = f"submitted_{current_index}"
        if submitted_key not in st.session_state:
            # Directly display the answer options.
            answer = st.radio("Select your answer:", question["options"], key=f"q{current_index}")
            if st.button("Submit Answer", key=f"submit_{current_index}"):
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
    # Display the timer on the result page as well.
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
How It Works
Timer Setup:

The quiz duration is set to 1500 seconds (25 minutes).

When the user submits their details on the welcome page, the start time is stored in st.session_state["quiz_start_time"].

Timer Display:

The function display_timer() calculates the remaining time, displays it (in MM:SS format) at the top right of the quiz (and result) page, and if the remaining time is zero, automatically sets the quiz index to the total number of questions (thus treating unanswered questions as wrong) before rerunning the app.

Auto Skip on Time Expiry:

Once the timer runs out, the quiz page is refreshed to show the result page with any unanswered questions left as incorrect.

Feel free to adjust any styling or timer parameters as needed. Enjoy your quiz app with the new 25‑minute timer!

if i need to remove function of skip quize which code part nee to hide from app for remove skip quize function tell me line number to line number
Syed, the skip‐quiz functionality in the code is isolated in a clearly marked block within the quiz() function. Specifically, you'll see comments like:

python
# SKIP BUTTON for testing; remove if not needed.
if st.button("Skip Quiz", key="skip_quiz"):
     st.session_state["current_index"] = len(questions)
# SKIP BUTTON END
If you want to remove the skip function entirely, simply remove or comment out this block. In the version of the code I provided above, this block appears within the quiz() function. (Your exact line numbers might vary depending on formatting, but if you search for the comment "# SKIP BUTTON for testing; remove if not needed." you'll find the block that needs to be removed.)

For instance, if your file shows these lines from, say, line 100 to line 103, then you should remove lines 100–103.

Let me know if you need further help!

KeyError: 'options' Traceback: File "C:\Users\Laptroncs.co\Documents\MEGA\python_quizApp\main.py", line 267, in <module> main() ~~~~^^ File "C:\Users\Laptroncs.co\Documents\MEGA\python_quizApp\main.py", line 264, in main quiz() ~~~~^^ File "C:\Users\Laptroncs.co\Documents\MEGA\python_quizApp\main.py", line 202, in quiz answer = st.radio("Select your answer:", question["options"], key=f"q{current_index}") ~~~~~~~~^^^^^^^^^^^
This error means that when the code is trying to access question["options"], that key is missing in one (or more) of your question objects coming from your questions.json file.

Steps to resolve:

Verify your JSON structure: Open your questions.json file and ensure that each question object has an "options" key. The expected structure is something like:

json
{
  "question": "What is the capital of France?",
  "options": ["Paris", "Rome", "Madrid", "Berlin"],
  "answer": "Paris"
}
If your questions use a different key (for example, "choices" instead of "options"), you have two choices:

Update the JSON file to include "options" in each object, or

Update your code to use the key that you already have.

Add error-checking in the code: To safeguard against missing keys and diagnose the issue more clearly, you can add a check in your code. For example, in the quiz() function where you access question["options"], you can update it as follows:

python
if "options" not in question:
    st.error("Question format error: missing 'options' key for the current question.")
    return
answer = st.radio("Select your answer:", question["options"], key=f"q{current_index}")
This will provide a more informative error message on the screen if a question is missing the "options" key.

Review your questions.json file: Ensure every question includes the keys "question", "options", and "answer". If any question is missing one of these keys, update it accordingly.

Once you update your JSON file or adjust your code to refer to the correct key name, the error should be resolved.

Let me know if you need any further assistance or if you'd like me to help adjust the code!

i have main.py, imag.png, quetions.json now which files more i need to make ill upload in git and than streamlit
Syed, to deploy your Streamlit app successfully on GitHub (and later on Streamlit Cloud), besides your existing files—main.py, imag.png, and quetions.json (or "questions.json")—you’ll want to include a few additional files:

requirements.txt List all the Python packages your app depends on (for example, Streamlit and any others such as streamlit-autorefresh if you use it). This ensures that when your app is deployed, the correct dependencies are installed. For instance, your requirements.txt might look like this:

streamlit
streamlit-autorefresh
(Add any other library you use.)

.gitignore This file helps ensure that unwanted files (such as Python cache folders like __pycache__/ and virtual environment directories) are not uploaded to GitHub. A basic .gitignore for Python might include:

__pycache__/
*.pyc
.DS_Store
venv/
env/
README.md (Optional but recommended) A README file provides an overview of your project, instructions on how to run it locally, and details on how to deploy it. This will be useful both for others and for your own reference.

Once you commit and push these files to GitHub, platforms like Streamlit Cloud will automatically detect your app (by looking for main.py or app.py) and install the listed dependencies in your requirements.txt file.

That’s all! With these files in your repository, you should have everything you need to deploy your Streamlit quiz app.

how to make requirements.txt
A requirements.txt file lists your app's dependencies so that when someone (or a deployment platform like Streamlit Cloud) installs your project, all needed packages & versions are set up. Here’s how you can create one:

Option 1: Manually Create a requirements.txt File
Open your text editor: Create a new file called requirements.txt in your project directory.

List the dependencies: Add one package per line. For example, if your quiz app uses Streamlit and streamlit-autorefresh, your file might look like:

streamlit
streamlit-autorefresh
Save the file: Commit and push requirements.txt to your GitHub repository.

Option 2: Automatically Generate with pip
If you're working in a virtual environment and have only installed the packages your app uses, you can generate a requirements.txt by running the following command in your terminal:

bash
pip freeze > requirements.txt
This command writes every package and its version installed in your environment to requirements.txt. Note: This file may list more packages than necessary if your environment has extras that your app doesn’t need. In that case, you might want to manually edit the file to keep only the required dependencies.

Best Practices
Version Pinning: Sometimes you might want to specify versions to ensure consistency. For example:

streamlit==1.15.0
streamlit-autorefresh==0.1.3
Keep It Lean: Only list the packages required by your application so that deployments are fast and predictable.

Once your requirements.txt is in your GitHub repository, platforms like Streamlit Cloud will automatically install these packages when they deploy your app.

Feel free to ask if you need further clarification!

is it posible when i upload oin streamlit data will be collect auto metically data( user inputed name role number)
By default, Streamlit doesn't store or log user inputs like name or roll number—you get access to them in memory (via session state) only during the user’s session. If you want to "collect" (log/persist) that data automatically (for example, saving it to a file or database), you'll need to implement that explicitly in your app.

For instance, you could write the user’s input to a CSV file or connect your app to a database (SQL, Firebase, etc.) so that each submission is recorded. Here’s a simple example of writing the data to a CSV file when the user submits the form:

python
import csv

def save_user_data(name, roll):
    # Open a CSV file in append mode.
    with open("user_data.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, roll, time.strftime("%Y-%m-%d %H:%M:%S")])
Then call save_user_data(name, roll) in your welcome form submission after validating the input.

Keep in mind that when you deploy your app (for instance, on Streamlit Cloud), you'll need to ensure that you have permission to write files or that you’re connecting to a database or another external storage service (and configure credentials accordingly).

So, while it’s definitely possible to collect input data automatically, you'll have to add that storage logic yourself. Let me know if you need help integrating one of these approaches into your app!

can i upload on github and posted on streamlit but can i add restructions on my git repo that no body can see my repo but app will run on streamlit samothly
Yes, you can keep your GitHub repository private while still deploying your app on Streamlit Cloud. Here are a few details and steps to help you understand how:

Private GitHub Repositories: You can create a private repository in GitHub. Only you (and collaborators you invite) will have access to the code. This means people won’t be able to see your source code when they visit your repository URL.

Deploying from a Private Repo: Streamlit Cloud supports deployments from private repositories. When setting up your app on Streamlit Cloud, you’ll have the option to link your GitHub account and grant access to your private repositories. Once linked, you can choose your private repo to deploy your app, and Streamlit Cloud will fetch your code and run it—even though the repo is not publicly visible.

Steps to Deploy:

Create or use a private repo: Make sure your app (including main.py, imag.png, questions.json (or quetions.json depending on your naming), and requirements.txt) is in a private repository on GitHub.

Set up a requirements.txt: This file tells Streamlit Cloud what dependencies to install.

Link GitHub with Streamlit Cloud: In your Streamlit Cloud dashboard, when you create a new app, connect your GitHub account and select your private repository.

Grant permissions: Approve any permission requests so that Streamlit Cloud can access your private repo.

Visibility: Your repository remains private, and only authorized collaborators can see it on GitHub. However, your app will be publicly accessible on the URL provided by Streamlit Cloud unless you configure additional restrictions there.

So, in short, yes—you can do exactly that. Just ensure you configure your GitHub repository as private and link it properly to your Streamlit Cloud deployment. This way, your code stays hidden from public view while your app runs and is accessible on Streamlit Cloud.

Let me know if you need more details on any of these steps!

share read me file for this app
Below is a sample README.md file you can include in your repository. You can copy and paste it into a file named README.md and then commit it to your GitHub repository. This file explains the project, its requirements, how to run it locally, and additional details about deployment.

markdown
# Python MCQ Quiz App

This is a Streamlit-based Python quiz application designed for a multiple-choice quiz. Users enter their name and roll number to begin the quiz, and questions are loaded from a `questions.json` file. The app includes a 25-minute countdown timer that, when expired, automatically ends the quiz (unanswered questions are marked incorrect) and displays the results. The results page shows your score, percentage, and a progress circle that visually represents your performance.

## Features

- **User Input Page:**  
  Users provide their name and roll number before starting the quiz.

- **Dynamic Quiz Screen:**  
  Questions are displayed one-by-one with answer options loaded from `questions.json`.

- **Countdown Timer:**  
  A 25-minute timer is shown on every quiz and result page. Once time expires, the quiz auto-skips remaining questions and ends the session.

- **Results Display:**  
  The results page shows:
  - Total score
  - Percentage of correct answers
  - A progress circle (color-coded based on performance)

- **Custom Styling:**  
  The app uses a custom background (`imag.png`) with CSS styling tailored for a clean and responsive user interface.

- **Deployment Ready:**  
  Easily deployable on Streamlit Cloud. You can keep your GitHub repository private and still deploy your app publicly.

## Prerequisites

- Python 3.7 or higher
- [Streamlit](https://streamlit.io/)
Deployment on Streamlit Cloud
Push your repository to GitHub. You can keep your repository private.

Log in to Streamlit Cloud and connect your GitHub account.

Create a new app: Select your repository/branch and let Streamlit Cloud install dependencies automatically from requirements.txt.

Deploy! Your app will be deployed and publicly accessible (unless further restricted by the Streamlit Cloud settings).

Customization Options
Timer Duration: The quiz timer is set to 1500 seconds (25 minutes) in the app. Adjust the TOTAL_TIME variable in main.py as needed.

Skip Functionality: For testing, there's a "Skip Quiz" button. You can remove this code block if you don't want users to manually skip.

Data Collection: The app currently doesn't log user details permanently. You can add functionality (e.g., saving to a file or database) if needed."# streamlit__python_quizApp" 

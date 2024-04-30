import streamlit as st
import firebase_admin
from firebase_admin import db, credentials
from datetime import datetime

# Set page configuration
st.set_page_config(layout="wide")

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    try:
        # Initialize Firebase Admin SDK
        cred = credentials.Certificate("connected-3948a-firebase-adminsdk-zthtg-53ccdd7723.json")
        firebase_admin.initialize_app(cred, {"databaseURL": "https://connected-3948a-default-rtdb.firebaseio.com"})
    except Exception as e:
        st.error(f"Firebase initialization error: {e}")

# Set up Streamlit layout
if st.button("Back to Dashboard"):
    st.switch_page("pages/Dashboard.py")

# UI Header
st.markdown("""
    <h1 style='color: white;'>Connect<span style='color: yellow;'>Ed</span></h1>
    <h3>Book a meeting with mentor!</h3>
    <hr>
""", unsafe_allow_html=True)

# Read username from log.txt
with open("log.txt","r") as f:
    username = f.read().strip()

# Retrieve student data from Firebase
students_ref = db.reference("/students")
student_data = students_ref.get()

# Get student's data
student = None
for key, data in student_data.items():
    if data["username"] == username:
        student = data
        break

if student is None:
    st.error("Student data not found!")

# Get available meeting slots
meeting_slots = student["meetings"]

# Weekend options (Saturday and Sunday)
weekend_options = ["Saturday", "Sunday"]
selected_day = st.selectbox("Select a day for the meeting:", weekend_options)

# Slider for selecting meeting time
meeting_time = st.slider("Select meeting time (7:00 AM - 7:00 PM):", min_value=7, max_value=19, step=1)

if st.button("Fix a meet!"):
    # Check if selected day is weekend
    if selected_day in weekend_options:
        # Construct meeting timestamp
        meeting_datetime = datetime.strptime(f"{selected_day} {meeting_time}:00", "%A %H:%M")
        
        # Format meeting time
        meeting_slot = meeting_datetime.strftime("%I-%p").lstrip("0").replace(" 0", " ")

        # Update meeting slot if available
        if meeting_slot not in meeting_slots:
            meeting_slots.append(meeting_slot+" On "+selected_day)
            students_ref.child(key).update({"meetings": meeting_slots})
            st.success(f"Meeting booked with mentor! at {meeting_slots[-1]}")
        else:
            st.warning("Selected time slot is unavailable!")
    else:
        st.error("Please select a weekend day for the meeting!")

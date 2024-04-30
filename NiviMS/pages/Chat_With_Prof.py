import streamlit as st
import firebase_admin
from firebase_admin import db, credentials

# Set page configuration
st.set_page_config(layout="wide")

# Read username from log.txt
with open("log.txt", "r") as f:
    username = f.read().strip()

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
    <h3>Search Professors</h3>
""", unsafe_allow_html=True)

# Retrieve professors' names from Firebase
ref = db.reference("/mentors")
all_professors = ref.get()
professor_names = [all_professors[professor]["name"] for professor in all_professors]

# Select professor
selected_professor = st.selectbox("Choose Professor", professor_names)

# Display professor details
st.markdown("""<hr>""", unsafe_allow_html=True)
st.header(selected_professor)
st.caption("Last seen at 4:01pm")

# Chat input
message = st.chat_input("Send Message")

# Send message to Firebase
if message:
    # Create or get chat history document for the selected professor and username
    chat_ref = db.reference(f"/chat/{selected_professor}/{username}")
    # Push message to chat history
    chat_ref.push({
        "sender": username,
        "message": message
    })
# Retrieve and display chat history
chat_history_ref = db.reference(f"/chat/{selected_professor}/{username}")
chat_history = chat_history_ref.get()

if chat_history:

    for key, message_data in chat_history.items():
        with st.chat_message("human"):    
            sender = message_data['sender']
            message = message_data['message']
            st.text(f"{sender}:")
            st.subheader(message)

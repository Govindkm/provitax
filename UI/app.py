# app.py

import streamlit as st
from auth import init_db, add_user, validate_user, user_exists
from PIL import Image

# Initialize the database
init_db()

# Manage user session
if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False
    st.session_state.username = None
    st.session_state.role = None

# Create a function for the registration page
def register():
    st.subheader("Create a New Account")

    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    email = st.text_input("Email")
    full_name = st.text_input("Full Name")
    role = st.selectbox("Select Role", ["SupportUser", "Customer"])  # Add role selection

    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        elif user_exists(username):
            st.error("Username already exists!")
        else:
            add_user(username, password, email, full_name, role)
            st.success("Account created successfully!")
            st.info("Go to the login page to access your account.")

# Create a function for the login page
def login():
    st.subheader("Login to Your Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_role = validate_user(username, password)  # Validate user and get their role
        if user_role:
            st.session_state.user_logged_in = True
            st.session_state.username = username
            st.session_state.role = user_role
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid username or password")

# Create a function to display the main application after login
def main_app():
    st.title(f"Welcome {st.session_state.username} to the Chatbot Application!")
    st.text("This is the main app page where you can access your chatbot interface.")

    # Display different options based on user role
    if st.session_state.role == "SupportUser":
        st.sidebar.header("Support User Menu")
        st.sidebar.button("Manage Users")
        st.sidebar.button("View Logs")
        st.write("You have SupportUser access. You can manage users and view logs.")
        # Implement more SupportUser-specific functionalities here...
    elif st.session_state.role == "Customer":
        st.sidebar.header("Customer Menu")
        st.sidebar.button("Chat with Bot")
        st.write("You have Customer access. You can chat with the bot and view your history.")
        # Implement more Customer-specific functionalities here...

    # Option to logout
    if st.button("Logout"):
        st.session_state.user_logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.success("Logged out successfully.")

# Page navigation logic
# Sidebar logo and configuration
st.sidebar.title("Provitax Menu")
logo_path = "C:\\Users\\GOVIN\\Desktop\\provitax\\UI\\static\\provitaxlogo.png"  # Update with your logo path
if logo_path:
    logo = Image.open(logo_path)
    st.sidebar.image(logo, width=150)
page = st.sidebar.selectbox("Choose a page", ["Login", "Register", "Main App"])

if page == "Login":
    if not st.session_state.user_logged_in:
        login()
    else:
        main_app()

elif page == "Register":
    register()
elif page == "Main App":
    if st.session_state.user_logged_in:
        main_app()
    else:
        st.warning("Please login first.")
        login()

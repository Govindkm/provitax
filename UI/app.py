import streamlit as st
from auth import init_db, add_user, validate_user, user_exists, add_chat_history, update_chat_history
from PIL import Image
import json

# Set the theme
st.set_page_config(
    page_title='ProviTax-Assistant',
    layout='wide',
    initial_sidebar_state='expanded',
    # theme={
    #     'primaryColor': '#FFA500',  # Orange color for the sidebar
    #     'backgroundColor': '#87CEEB',  # Light sky blue color for the main app area
    #     'secondaryBackgroundColor': '#FFA500',  # Orange color for the sidebar background
    #     'textColor': '#000000',  # Black text color
    #     'font': 'sans serif'
    # }
)

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

# Function to initialize chat session state
def initialize_chat():
    if "messages" not in st.session_state:
        st.session_state.chat_id = -1
        st.session_state.messages = []

# Function to display chat messages from session state
def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
             # Check if metadata exists and display it
            if "metadata" in message and message["metadata"]:
                st.write("**References:**")
                for ref in message["metadata"]:
                    st.markdown(f"- [{ref['info']}]({ref['url']})")

# Function to handle user input and update chat history
def handle_user_input():
    # Read user input from chat
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate chatbot response (call a separate function to handle this)
        response = generate_response(prompt)

        # Add chatbot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response['message'], "metadata": response.get("metadata")})

        # Display chatbot's response
        st.chat_message("assistant").markdown(response)

# Placeholder function to generate chatbot response (replace with model call)
def generate_response(prompt):
    # You can replace this with an actual chatbot model's response
    response_metadata = [
        {"info": "Reference 1", "url": "https://example.com/reference1"},
        {"info": "Reference 2", "url": "https://example.com/reference2"}
    ]
    return {"message": f"This is a placeholder response to the message: {prompt}", "metadata": response_metadata}

# Create a function to display the main application after login
def main_app():
    st.title(f"Welcome to ProvitaxAI")
    st.text("Revolutionizing Tax Provision Support")

    # Display different options based on user role
    if st.session_state.role == "SupportUser":
        st.sidebar.header("Support User Menu")
        st.sidebar.button("Manage Users")
        st.sidebar.button("View Logs")
        st.write("ProviTax  uses generative AI to answer questions based on user guides, help articles, previous customer cases, view logs, ITR creation process, and release notes. Ask a detailed question about a tax provision product to get started.")
        # Implement more SupportUser-specific functionalities here...
    elif st.session_state.role == "Customer":
        st.sidebar.header("Customer Menu")
        st.sidebar.button("Chat with Bot")
        st.write("ProviTax uses generative AI to answer questions based on user guides, help articles, and release notes. Ask a detailed question about a tax provision product to get started.")
        # Implement more Customer-specific functionalities here...
        
    initialize_chat()      # Initialize chat session state
    handle_user_input()    # Handle user input and generate response
    display_chat_messages()# Display chat history
        
    # Option to logout on the top right corner
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        # ToDo: Save Chat History to Database
        
        chat_history_json = json.dumps(st.session_state.messages)
        
        if st.session_state.chat_id == -1:
            st.session_state.chat_id = add_chat_history(st.session_state.username, chat_history_json)
        else:
            update_chat_history(st.session_state.chat_id, chat_history_json)
        # ToDo:  Redirect UI to login page
        st.session_state.user_logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()
        st.success("Logged out successfully.")

# Page navigation logic
# Sidebar logo and configuration
st.markdown(
    f"""
    <style>
    .stSidebar {{
        background-color: #ffefce;  /* Light orange color */
    }}
    </style>
    """, unsafe_allow_html=True
)
st.sidebar.title("Provitax Menu")
logo_path = "C:\\Users\\GOVIN\\Desktop\\provitax\\UI\\static\\provitaxlogo.png"  # Update with your logo path
if logo_path:
    logo = Image.open(logo_path)
    st.sidebar.image(logo, width=150)
page = st.sidebar.selectbox("Choose a page", ["Login", "Register", "Home", "FAQ"])

if page == "Login":
    if not st.session_state.user_logged_in:
        login()
    else:
        main_app()

elif page == "Register":
    register()
elif page == "Home":
    if st.session_state.user_logged_in:
        main_app()
    else:
        st.warning("Please login first.")
        login()

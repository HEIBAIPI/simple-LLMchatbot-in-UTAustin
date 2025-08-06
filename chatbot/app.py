# app.py

import streamlit as st
from chatbot_logic import FriendlyBot, TeacherBot

# --- Page Configuration ---
st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 UTBot: Your AI Chat Companion")
st.write("Choose a personality from the sidebar and start chatting!")

# --- Sidebar for Bot Selection and Control ---
with st.sidebar:
    st.header("Configuration")

    # Initialize bot in session state if not present
    if 'bot' not in st.session_state:
        st.session_state.bot = None

    bot_choice = st.radio(
        "Choose your chatbot personality:",
        ('Friendly', 'Teacher'),
        key="bot_choice_radio",
        disabled=(st.session_state.bot is not None) # Disable after selection
    )

    subject = ""
    if bot_choice == 'Teacher':
        subject = st.text_input(
            "What subject should the teacher focus on?",
            "Quantum Mechanics",
            key="subject_input",
            disabled=(st.session_state.bot is not None)
        )
        bot_name = st.text_input(
           "What is the teacher's name?",
           "Albert",
           key="name_input",
           disabled=(st.session_state.bot is not None)
        )

    if st.button("Start Chat", key="start_button", disabled=(st.session_state.bot is not None)):
        if bot_choice == 'Friendly':
            st.session_state.bot = FriendlyBot(name="Joy")
        else:
            if subject and bot_name:
                st.session_state.bot = TeacherBot(name=f"Professor {bot_name}", subject=subject)
            else:
                st.warning("Please enter BOTH a subject and a name for the Teacher Bot.")
                st.stop()
        
        # Initialize chat history
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]
        st.rerun()

    if st.session_state.bot is not None:
        if st.button("Reset Conversation", key="reset_button"):
            st.session_state.bot = None
            st.session_state.messages = []
            st.rerun()

# --- Main Chat Interface ---
if 'bot' in st.session_state and st.session_state.bot is not None:
    # Display chat messages
    for message in st.session_state.get('messages', []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What would you like to say?"):
        # Add user message to display history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.bot.generate_response(prompt)
                st.markdown(response)
        
        # Add assistant response to display history
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("Please configure your chatbot in the sidebar and click 'Start Chat'.")
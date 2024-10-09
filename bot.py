import streamlit as st
from utils import write_message
from agent import generate_response

# Page Config
st.set_page_config("Neo4j LLM Movie Agent", page_icon=":movie_camera:")

st.write("# Welcome to the Neo4j LLM Movie Chatbot! 🎬")

# Example questions
example_questions = [
    "Tell me about The Matrix.",
    "Who directed Inception?",
    "What are some popular movies from the 90s?",
    "Can you recommend a sci-fi movie?",
    "Who starred in The Godfather?"
]

# Submit handler


def handle_submit(message):
    # Handle the response
    with st.spinner('Thinking...'):
        # Call the agent
        response = generate_response(message)
        write_message('assistant', response)


# Display example questions as buttons
st.subheader("Example Questions")
for question in example_questions:
    if st.button(question):
        st.session_state.clicked_question = question

# Set up Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
            "content": "Hi, I'm the Neo4j LLM Movie Agent! How can I help you?"},
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Process clicked sample question
if "clicked_question" in st.session_state:
    input = st.session_state.clicked_question
    # Clear the clicked question after processing
    del st.session_state.clicked_question
    st.session_state.messages.append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.write(input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking ..."):
            response = generate_response(input)
            st.session_state.messages.append(
                {"role": "assistant", "content": response})
            st.write(response.replace('\n', ' '))

# User-provided prompt
if input := st.chat_input():
    if input.strip():
        st.session_state.messages.append({"role": "user", "content": input})
        with st.chat_message("user"):
            st.write(input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking ..."):
                response = generate_response(input)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response})
                st.write(response.replace('\n', ' '))

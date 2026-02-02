import streamlit as st
from openai import OpenAI

# OpenAI client using Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API key missing!")
    st.stop()

st.set_page_config(
    page_title="GPT-4o Chat",
    page_icon="💬",
    layout="centered"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🤖 GPT-4o - ChatBot")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask GPT-4o...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_prompt
    })

    with st.spinner("GPT-4o is thinking..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *st.session_state.chat_history
            ],
            temperature=0.7
        )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": assistant_response
    })

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
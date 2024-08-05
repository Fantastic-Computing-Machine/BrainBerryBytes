import streamlit as st
# from agent import financial_react_agent
from ai71_model import AI71Model
from message_history import MessageHistory
from scripts import TherapyScript

AGENT_NAME = "BrainBerryBytes"

# Streamlit UI configuration
st.set_page_config(
    page_title=AGENT_NAME,
    page_icon="💸💰",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        # "Report a bug": "https://github.com/adiagarwalrock/finvest-ai/issues",
        # "About": "Finvest AI leverages cutting-edge AI technology to provide instant and comprehensive financial insights.",
    },
)

st.title(f"{AGENT_NAME} 💸💰")
st.caption(f"🤖 Chat with {AGENT_NAME} 🔌 by FCM")


if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": f"Hi! I am your friendly therapist B3.",
        }
    ]


if "therapy_bot" not in st.session_state.keys():  # Initialize the chat engine
    history_session = MessageHistory()
    st.session_state.therapy_bot = TherapyScript(model= AI71Model(), args={}, history=history_session)

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response_stream = st.session_state.therapy_bot.submit_query(prompt).content
        st.write(response_stream)
        message = {"role": "assistant", "content": response_stream}
        st.session_state.messages.append(message)
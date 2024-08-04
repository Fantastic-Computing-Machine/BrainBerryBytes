from groq import Groq
import streamlit as st
# from agent import financial_react_agent
import streamlit as st
import requests
import tempfile
from pydub import AudioSegment
import time
from st_audiorec import st_audiorec
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from ai71_model import AI71Model
from message_history import MessageHistory
from utility.speech_to_text import SpeechToText
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from utility.speech_to_text import SpeechToText

AGENT_NAME = "BRAIN BERRY BYTES"
history = MessageHistory()
ai71 = AI71Model()
# Streamlit UI configuration
st.set_page_config(
    page_title=AGENT_NAME,
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "Report a bug": "https://github.com/adiagarwalrock/finvest-ai/issues",
        "About": "Finvest AI leverages cutting-edge AI technology to provide instant and comprehensive financial insights.",
    },
)

st.title(f"{AGENT_NAME} 🧠")
st.caption(f"🤖 Chat with {AGENT_NAME} 🔌 by Y-Finance and Llama3")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": f"Hi! I am your friendly metal head assistant, {AGENT_NAME}. How can I help you today?",
        }
    ]

speech_to_text = SpeechToText()
audio_bytes = audio_recorder(
    text="",
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_name="microphone",
    icon_size="2x",
)
print("st.session_state.messages->",st.session_state.messages)
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    prompt = speech_to_text.convert(audio_bytes)
    st.session_state.messages.append({"role": "user", "content": prompt})
    # st.chat_input(Your question)
else :
    prompt = st.chat_input("Your question")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
print("--------")
for message in st.session_state.messages:
    print("message->",message, "->",message["role"])
    with st.chat_message(message["role"]):
        st.write(message["content"])
print("--------")
if st.session_state.messages[-1]["role"] != "assistant":
    print("assistanting ...")
    with st.chat_message("assistant"):
        print("prompt->",prompt)
        response_stream = ai71.chat(prompt, history)
        print("response_stream->",response_stream)
        st.write(response_stream)
        message = {"role": "assistant", "content": response_stream}
        st.session_state.messages.append(message)
print("********")
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
from utility.speech_to_text import SpeechToText
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from utility.speech_to_text import SpeechToText

AGENT_NAME = "Finvest AI"

# Streamlit UI configuration
st.set_page_config(
    page_title=AGENT_NAME,
    page_icon="💸💰",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "Report a bug": "https://github.com/adiagarwalrock/finvest-ai/issues",
        "About": "Finvest AI leverages cutting-edge AI technology to provide instant and comprehensive financial insights.",
    },
)

st.title(f"{AGENT_NAME} 💸💰")
st.caption(f"🤖 Chat with {AGENT_NAME} 🔌 by Y-Finance and Llama3")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": f"Hi! I am your friendly neighborhood financial analyst",
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

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    transcription_text = speech_to_text.convert(audio_bytes)
    st.session_state.messages.append({"role": "user", "content": transcription_text})
    # st.chat_input(transcription_text)

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        # Replace this with the actual response stream from your agent
        response_stream = "Some response stream"
        st.write(response_stream)

        message = {"role": "assistant", "content": response_stream}
        st.session_state.messages.append(message)

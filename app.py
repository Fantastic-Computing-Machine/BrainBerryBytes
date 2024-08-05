import streamlit as st
# from agent import financial_react_agent
from ai71_model import AI71Model
from message_history import MessageHistory
from scripts import TherapyScript

AGENT_NAME = "BrainBerryBytes"

def validate_ai71_key(api_key):
    if api_key == "":
        return False
    try:
        AI71Model(api_key=api_key).chat()
        return True
    except:
        return False

def validate_groq_key(api_key):
    if api_key == "":
        return False
    try:
        # Assuming there's a similar method to validate Groq key
        # Placeholder for actual validation
        return True
    except:
        return False

# Streamlit UI configuration
st.set_page_config(
    page_title=AGENT_NAME,
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        # "Report a bug": "https://github.com/adiagarwalrock/finvest-ai/issues",
        # "About": "Finvest AI leverages cutting-edge AI technology to provide instant and comprehensive financial insights.",
    },
)

st.title(f"{AGENT_NAME} 🧠")
st.caption(f"🤖 Chat with {AGENT_NAME} 🔌 by FCM")

# Initialize the chat messages history if not already done
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"Hi! I am your friendly therapist B3."}
    ]

# Sidebar for API keys input with separate submit buttons
with st.sidebar:
    with st.form(key='ai71_key_form'):
        AI71_key = st.text_input("AI71 API Key", placeholder="ai71-api...")
        submit_ai71_button = st.form_submit_button(label='Submit AI71 Key')

    if submit_ai71_button:
        if not validate_ai71_key(AI71_key):
            st.error("Valid AI71 API key is necessary for your Therapist 😊")
        else:
            st.session_state.valid_ai71_key = True
            st.session_state.ai71_key = AI71_key  # Store the valid AI71 key

    with st.form(key='groq_key_form'):
        Groq_key = st.text_input("Voice API Key", placeholder="powered by Groq")
        submit_groq_button = st.form_submit_button(label='Submit Groq Key')

    if submit_groq_button:
        if not validate_groq_key(Groq_key):
            st.error("Invalid Groq API key")
        else:
            st.session_state.valid_groq_key = True
            st.session_state.groq_key = Groq_key  # Store the valid Groq key

if st.session_state.get('valid_ai71_key', False):
    if "therapy_bot" not in st.session_state:
        history_session = MessageHistory()
        st.session_state.therapy_bot = TherapyScript(model=AI71Model(api_key=st.session_state.ai71_key), args={}, history=history_session)

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

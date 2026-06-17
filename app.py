import io
import streamlit as st
from google import genai
from google.genai import types
from gtts import gTTS

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("Gemini 3.1 Flash Chatbot 🚀")
st.caption("Type your message or click the microphone icon inside the box to speak!")

# --- STEP 1: SAFE API KEY HANDLING (Fallback Chain) ---
# Check if secrets.toml exists. If it doesn't, we don't throw an error; we just default to None.
secrets_key = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        secrets_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    # This catches instances where .streamlit/secrets.toml doesn't exist at all
    pass

# Setup the sidebar interface
with st.sidebar:
    st.header("Settings ⚙️")
    
    # If the key was found in secrets, we use it as the default/placeholder
    if secrets_key:
        api_key = st.text_input(
            "Google Gemini API Key:", 
            value=secrets_key, 
            type="password",
            help="Loaded securely from secrets.toml"
        )
        st.success("API Key loaded from local secrets!")
    else:
        # If secrets.toml is missing, the field is blank and prompts the user
        api_key = st.text_input(
            "Enter Google Gemini API Key:", 
            type="password",
            placeholder="AIzaSy..."
        )
        st.info("💡 Tip: You can skip typing this by creating a `.streamlit/secrets.toml` file.")
        st.markdown("[Get a free key from Google AI Studio](https://aistudio.google.com/)")

# Block execution until an API key is available via either method
if not api_key:
    st.warning("Please provide a Gemini API Key in the sidebar to wake up the chatbot.", icon="🔑")
    st.stop()


client = genai.Client(api_key=api_key)

# Maintain Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat exchanges
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- THE UNIFIED INPUT BOX ---
# accept_audio=True blends the text field and the mic icon together at the bottom
prompt = st.chat_input("Type a message or record audio...", accept_audio=True)

if prompt:
    # 1. Determine if the user used Voice or Text
    is_voice = prompt.audio is not None
    user_content = []
    
    # Render the user's action in the UI
    with st.chat_message("user"):
        if is_voice:
            audio_bytes = prompt.audio.read()
            st.markdown("🗣️ *Sent a voice message:*")
            st.audio(audio_bytes, format="audio/wav")
            
            # Prepare audio data for Gemini
            user_content.append(types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"))
            user_content.append("Listen to this audio clip and reply to it concisely.")
            st.session_state.messages.append({"role": "user", "content": "🗣️ *Sent a voice message*" })
        else:
            st.markdown(prompt.text)
            user_content.append(prompt.text)
            st.session_state.messages.append({"role": "user", "content": prompt.text})

    # 2. Get Response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("AI is compiling response..."):
            try:
                response = client.models.generate_content(
                    model='gemini-3.1-flash-lite', 
                    contents=user_content,
                    config=types.GenerateContentConfig(
                        system_instruction="You are a professional corporate assistant. Keep answers brief and conversational."
                    )
                )
                
                ai_text = response.text
                st.markdown(ai_text)
                
                # 3. Convert response text to spoken audio locally using gTTS
                tts = gTTS(text=ai_text, lang='en', tld='com')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                ai_audio_bytes = fp.read()
                
                # Autoplay the spoken answer back to the user
                st.audio(ai_audio_bytes, format="audio/mp3", autoplay=True)
                
                # Save assistant memory
                st.session_state.messages.append({"role": "assistant", "content": ai_text})

            except Exception as e:
                st.error(f"An error occurred: {e}")
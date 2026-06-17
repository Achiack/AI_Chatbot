import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("Gemini 3.1 Flash Chatbot 🚀")
st.caption("Powered by Google AI Studio Free Tier")

# 1. Initialize Sidebar for API Key
with st.sidebar:
    default_key = ""
    try:
        if "API_KEY" in st.secrets:
            default_key = st.secrets["API_KEY"]
    except Exception:
        pass
    
    api_key = st.text_input(
        "Enter Google Gemini API Key:", 
        value=default_key, 
        type="password"
    )
    st.markdown("[Get a free key from Google AI Studio](https://aistudio.google.com/)")

# 2. Maintain Chat History in Streamlit Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages (This keeps the chat interface visible)
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Guard Rail: Stop execution HERE if there is no API Key
if not api_key:
    st.info("Please add your Gemini API key in the sidebar to continue.", icon="🔑")
    st.stop()

# Initialize the Google GenAI Client (Only runs if API key is present)
client = genai.Client(api_key=api_key)

# 4. Setup System Instructions 
system_instruction = "You are a helpful, professional workplace AI assistant. Keep responses concise."

# 5. Handle User Input
if prompt := st.chat_input("Ask me anything..."):
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Format history into the structure Google expects
    google_contents = []
    for msg in st.session_state.chat_history:
        role = "user" if msg["role"] == "user" else "model"
        google_contents.append(types.Content(
            role=role, 
            parts=[types.Part.from_text(text=msg["content"])]
        ))
    
    # Add the newest user prompt to the list
    google_contents.append(types.Content(role="user", parts=[types.Part.from_text(text=prompt)]))
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # 5. Generate Response using Gemini 3.5 Flash
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Call the stream API for that nice typewriter effect
            response_stream = client.models.generate_content_stream(
                model='gemini-3.1-flash-lite',
                contents=google_contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                )
            )
            
            for chunk in response_stream:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
                
            response_placeholder.markdown(full_response)
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
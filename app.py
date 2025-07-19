import streamlit as st
from modules.ollama import build_vectorstore_from_text, get_chat_chain
from modules.youtube_utils import extract_video_id, get_transcript

st.set_page_config(page_title="Youtube Assistant", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_chain" not in st.session_state:
    st.session_state.chat_chain = None

# --- Sidebar: Input YouTube URL ---
st.sidebar.title("🎥 YouTube Assistant")
video_url = st.sidebar.text_input("Paste YouTube video URL:")

@st.cache_resource(show_spinner=False)
def process_video(video_id, transcript):
    vectorstore = build_vectorstore_from_text(transcript)
    return get_chat_chain(vectorstore)

if video_url:
    try:
        video_id = extract_video_id(video_url)
        st.sidebar.success(f"Video ID: {video_id}")

        if st.session_state.get("loaded_video_id") != video_id:
            with st.spinner("Fetching transcript..."):
                transcript = get_transcript(video_id)

            if "current_video_id" not in st.session_state or st.session_state.current_video_id != video_id:
                with st.spinner("Building vector store and QA chain..."):
                    st.session_state.chat_chain = process_video(video_id, transcript)
                    st.session_state.chat_history = []  # reset chat for new video
                    st.session_state.current_video_id = video_id

            st.success("Ready! Ask your questions below 👇")

    except Exception as e:
        st.error(f"Error: {str(e)}")

# --- Main Chat UI ---
st.title("💬 Chat About the YouTube Video")

if st.session_state.chat_chain:
    user_input = st.chat_input("Ask a question about the video...")

    if user_input:
        with st.spinner("Thinking..."):
            response = st.session_state.chat_chain.invoke({
                "question": user_input,
                "chat_history": st.session_state.chat_history
            })
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("assistant", response["answer"]))

    # Display chat history
    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)
else:
    st.info("Paste a YouTube URL in the sidebar to begin.")
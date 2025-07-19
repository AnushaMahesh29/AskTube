# AskTube
---

AskTube is a simple AI tool that lets you ask questions about any YouTube video. The application retrieves the video transcript, converts it into embeddings, and uses a local Large Language Model (LLM) to answer user queries in real time. It is built using the RAG (Retrieval-Augmented Generation) architecture, integrating LangChain, FAISS, Ollama, and Streamlit for a seamless and private user experience 

---

##  What It Does

- Paste a YouTube video link
- Automatically fetches the transcript
- Uses AI (via Ollama + LangChain) to answer your questions about the video
- Runs entirely locally with no external API calls

---

##  How It Works

1. **Transcript**: Extracts the transcript using `youtube-transcript-api`
2. **Text Processing**: Splits the text into chunks
3. **Embeddings**: Converts text into vectors using `all-minilm`
4. **LLM**: Uses a local LLM (like `phi3` or `llama3`) through Ollama
5. **Chat**: You ask questions and it answers based on the video content

---

##  Tech Stack

- **Frontend**: Streamlit
- **LLM**: Ollama (local model like llama3 or phi3)
- **LangChain**: For building the chat system
- **FAISS**: For storing and retrieving vectorized chunks
- **Embeddings**: all-minilm via Ollama
- **Transcript API**: youtube-transcript-api

---

##  Getting Started

1. **Install dependencies**
```bash      
pip install -r requirements.tx
```
2. **Start Ollama and pull models**
```bash  
ollama run llama3
ollama pull all-minilm
```
3. **Run the app**
```bash  
streamlit run app.py
```
##  Conclusion 
This project showcases how Retrieval-Augmented Generation (RAG) can be used to build practical AI tools by combining local LLMs, YouTube transcripts, and a simple UI. It runs entirely offline, respects user privacy, and demonstrates the power of open-source LLMs.



from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import ollama


def build_vectorstore_from_text(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = splitter.create_documents([text])
    embeddings = OllamaEmbeddings(model="all-minilm")

    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

def get_chat_chain(vectorstore):
    retriever = vectorstore.as_retriever()
    llm = ollama.Ollama(model="llama3")
    memory = None   

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory

    )
    return chain
    
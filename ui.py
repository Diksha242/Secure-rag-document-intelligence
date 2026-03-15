import streamlit as st
import os
import tempfile
import time
from rag_engine import RAGEngine

os.environ['NO_PROXY'] = '127.0.0.1,localhost'

st.set_page_config(
    page_title="Secure RAG Document Intelligence",
    page_icon="📄",
    layout="wide"
)

st.title("Chat with document")
st.caption("Offline AI assistant using Ollama + ChromaDB")


if "engine" not in st.session_state:

    with st.spinner("Initializing AI Engine..."):

        st.session_state.engine = RAGEngine()

if "chain" not in st.session_state:
    st.session_state.chain = None

if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:

    st.header("Upload your pdfs")

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:

        if st.button("Process Documents"):

            with st.spinner("Indexing documents..."):

                progress = st.progress(0)

                temp_dir = tempfile.mkdtemp()

                for i,file in enumerate(uploaded_files):

                    file_path = os.path.join(temp_dir,file.name)

                    with open(file_path,"wb") as f:
                        f.write(file.read())

                    progress.progress((i+1)/len(uploaded_files))

                chunks = st.session_state.engine.ingest_folder(temp_dir)

                st.session_state.chain = st.session_state.engine.get_chain()

            st.success(f"{chunks} chunks indexed")

    if st.button("Clear Chat"):
        st.session_state.messages = []


st.subheader("Chat With Your Documents")


if st.session_state.chain is None:

    st.info("Upload PDFs and click **Process Documents** to begin.")

else:

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.write(msg["content"])


    prompt = st.chat_input("Ask something about your documents...")

    if prompt:

        st.session_state.messages.append(
            {"role":"user","content":prompt}
        )

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):

            response_container = st.empty()

            with st.spinner("Searching documents..."):

                response = st.session_state.chain.invoke(prompt)

            streamed_text=""

            for word in response.split():

                streamed_text += word + " "

                response_container.markdown(streamed_text)

                time.sleep(0.02)

        st.session_state.messages.append(
            {"role":"assistant","content":response}
        )
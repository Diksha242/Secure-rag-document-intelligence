import os
import re
import time
import shutil
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

DB_DIR = "vector_db"
MODEL_NAME = "llama3.2:1b"


class RAGEngine:

    def __init__(self):

        self.local_url = "http://127.0.0.1:11434"

        print(f"\n--- Initializing {MODEL_NAME} ---")

        self.embeddings = OllamaEmbeddings(
            model=MODEL_NAME,
            base_url=self.local_url
        )

        self.llm = OllamaLLM(
            model=MODEL_NAME,
            temperature=0.1,
            base_url=self.local_url
        )

        self.vectorstore = None

        print("--- AI components ready ---")


    def clean_text(self, text):

        text = re.sub(r'\s+', ' ', text)
        return text.strip()


    def ingest_folder(self, folder_path):

        if os.path.exists(DB_DIR):
            try:
                shutil.rmtree(DB_DIR)
            except PermissionError:
                self.vectorstore = None
                time.sleep(1)
                shutil.rmtree(DB_DIR)

        all_docs = []

        files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

        if not files:
            print("No PDFs found")
            return 0

        for file_name in files:

            file_path = os.path.join(folder_path, file_name)

            loader = PyPDFLoader(file_path)

            docs = loader.load()

            all_docs.extend(docs)


        splitter = RecursiveCharacterTextSplitter(
            chunk_size=900,
            chunk_overlap=150
        )

        chunks = splitter.split_documents(all_docs)

        print(f"Creating embeddings for {len(chunks)} chunks")

        self.vectorstore = Chroma(
            persist_directory=DB_DIR,
            embedding_function=self.embeddings
        )

        batch_size = 25

        for i in range(0, len(chunks), batch_size):

            batch = chunks[i:i+batch_size]

            self.vectorstore.add_documents(batch)

            print(f"Indexed {min(i+batch_size,len(chunks))} chunks")


        print("Knowledge base ready")

        return len(chunks)


    def get_chain(self):

        if not self.vectorstore:

            self.vectorstore = Chroma(
                persist_directory=DB_DIR,
                embedding_function=self.embeddings
            )

        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k":5}
        )

        prompt = ChatPromptTemplate.from_template(
        """
You are a professional document assistant.

Use ONLY the context below to answer the question.

Always cite the document source using:

Source: <filename>, Page <number>

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""
        )


        def format_docs_with_sources(docs):

            formatted = []

            for d in docs:

                source = os.path.basename(d.metadata.get("source","Unknown"))

                page = d.metadata.get("page",0) + 1

                text = d.page_content

                formatted.append(
                    f"[Source: {source}, Page: {page}]\n{text}"
                )

            return "\n\n---\n\n".join(formatted)


        chain = (
            {
                "context": retriever | format_docs_with_sources,
                "question": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return chain
import os
import sys
from rag_engine import RAGEngine

# CRITICAL: Bypassing your system's corporate proxy for local AI communication
os.environ['NO_PROXY'] = '127.0.0.1,localhost'

def main():
    try:
        print("\n" + "="*50)
        print("   ADVANCED PDF INTELLIGENCE SYSTEM (LOCAL)")
        print("="*50)
       
        # 1. Initialize the Engine
        print("\n--- [1/3] Initializing AI Engine ---")
        engine = RAGEngine()
       
        # 2. Get Folder Path from User
        print("\n--- [2/3] Data Ingestion ---")
        folder_path = input("Enter the path to your PDF folder: ").strip()
       
        # Clean path formatting (removes quotes if copied from Windows Explorer)
        folder_path = folder_path.replace('"', '').replace("'", "")

        if os.path.isdir(folder_path):
            print(f"--- Processing directory: {folder_path} ---")
            num_chunks = engine.ingest_folder(folder_path)
           
            if num_chunks == 0:
                print("--- [!] No valid text extracted. Check your PDFs. ---")
                return
               
            print(f"--- [OK] Success: {num_chunks} chunks indexed into Vector DB ---")
        else:
            print(f"--- [!] Error: '{folder_path}' is not a valid directory ---")
            return

        # 3. Start the Retrieval-Augmented Chat
        chain = engine.get_chain()
        print("\n" + "="*50)
        print("--- RAG CHATBOT ACTIVE (Type 'exit' to quit) ---")
        print("="*50)
       
        while True:
            query = input("\nUser Query: ").strip()
           
            if not query:
                continue
            if query.lower() in ['exit', 'quit', 'bye']:
                print("Shutting down... Goodbye!")
                break
           
            print("AI is searching documents...")
            try:
                # Running the RAG chain
                response = chain.invoke(query)
               
                print("\n" + "-"*10 + " AI RESPONSE " + "-"*10)
                print(response)
                print("-" * 33)
               
            except Exception as chat_err:
                print(f"\n[Error during inference]: {chat_err}")
                print("Possible fix: Ensure 'ollama serve' is running in the background.")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting safely.")
    except Exception as e:
        print(f"\n[CRITICAL ERROR]: {e}")
        input("\nPress Enter to close the window...")

if __name__ == "__main__":
    main()
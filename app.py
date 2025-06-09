import streamlit as st
import tempfile
import os
from pdf_processor import PDFProcessor
from vector_store import VectorStore
from chat_engine import ChatEngine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="PDF Chat Assistant",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

# Initialize components only once
if not st.session_state.initialized:
    try:
        st.session_state.pdf_processor = PDFProcessor()
        st.session_state.vector_store = VectorStore()
        st.session_state.chat_engine = ChatEngine()
        st.session_state.initialized = True
    except Exception as e:
        st.error(f"Error initializing components: {str(e)}")
        st.stop()

# Main UI
st.title("📚 PDF Chat Assistant")
st.write("Upload a PDF and ask questions about its content!")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        # Process PDF
        with st.spinner("Processing PDF..."):
            # Get PDF info
            pdf_info = st.session_state.pdf_processor.get_pdf_info(tmp_path)
            st.write(f"📄 File: {pdf_info['filename']}")
            st.write(f"📑 Pages: {pdf_info['pages']}")
            st.write(f"📊 Size: {pdf_info['size'] / 1024:.2f} KB")

            # Process PDF and add to vector store
            chunks = st.session_state.pdf_processor.process_pdf(tmp_path)
            st.session_state.vector_store.add_documents(chunks, {"source": pdf_info['filename']})
            st.success("PDF processed successfully!")

        # Clean up temporary file
        os.unlink(tmp_path)

    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")

# Chat interface
if st.session_state.initialized:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your PDF"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Get relevant documents from vector store
                    relevant_docs = st.session_state.vector_store.similarity_search(prompt)
                    # Generate response using the chat engine
                    response = st.session_state.chat_engine.generate_response(prompt, relevant_docs)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}") 
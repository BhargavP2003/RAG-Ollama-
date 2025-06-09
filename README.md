# PDF Chat Assistant

A powerful RAG (Retrieval-Augmented Generation) application that allows you to chat with your PDF documents using Ollama and LangChain.

## Features

- PDF document processing and text extraction
- Vector-based semantic search using FAISS
- Chat interface powered by Ollama (using Llama2 model)
- Web UI built with Streamlit
- Document metadata tracking
- Conversation history

## Prerequisites

- Python 3.12 or higher
- Ollama installed and running locally
- Git (for version control)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd pdf-chat-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix/MacOS
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Make sure Ollama is running with the Llama2 model:
```bash
ollama run llama2
```

## Project Structure

- `app.py`: Main Streamlit application
- `chat_engine.py`: Chat engine implementation using Ollama
- `pdf_processor.py`: PDF processing and text extraction
- `vector_store.py`: Vector store implementation for semantic search
- `requirements.txt`: Project dependencies
- `fitness_guide.pdf`: Sample PDF for testing

## Dependencies

- streamlit>=1.32.0
- faiss-cpu>=1.7.4
- langchain>=0.1.0
- langchain-community>=0.0.10
- langchain-core>=0.1.10
- langchain-text-splitters>=0.0.1
- langchain-ollama>=0.0.1
- pypdf>=4.0.0
- ollama>=0.1.0
- numpy>=1.26.0
- scikit-learn>=1.4.0
- sentence-transformers>=2.2.2

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. Upload a PDF file using the file uploader

4. Wait for the PDF to be processed

5. Start asking questions about the PDF content in the chat interface

## How It Works

1. **PDF Processing**:
   - The PDF is uploaded and processed using PyPDF
   - Text is extracted and split into chunks
   - Each chunk is stored with its metadata

2. **Vector Store**:
   - Uses sentence-transformers to create embeddings
   - Implements semantic search using FAISS
   - Stores document chunks and their metadata

3. **Chat Engine**:
   - Powered by Ollama using the Llama2 model
   - Processes user queries and generates responses
   - Maintains conversation history

4. **Web Interface**:
   - Built with Streamlit
   - Provides file upload and chat interface
   - Displays conversation history and document information

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
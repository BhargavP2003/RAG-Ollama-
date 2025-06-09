from typing import List, Dict, Any
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import gc

class PDFProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file."""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def process_pdf(self, pdf_path: str) -> List[str]:
        """Process a PDF file and return chunks of text."""
        try:
            # Extract text from PDF
            text = self.extract_text_from_pdf(pdf_path)
            
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)
            
            # Clean up memory
            del text
            gc.collect()
            
            return chunks
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    def get_pdf_info(self, pdf_path: str) -> Dict[str, Any]:
        """Get basic information about a PDF file."""
        try:
            reader = PdfReader(pdf_path)
            return {
                "filename": os.path.basename(pdf_path),
                "pages": len(reader.pages),
                "size": os.path.getsize(pdf_path)
            }
        except Exception as e:
            raise Exception(f"Error getting PDF info: {str(e)}") 
from io import BytesIO
from typing import Optional
from docx import Document
import pdfplumber 

def extract_text_from_docx(file: BytesIO) -> str:
    """Extracts text from a DOCX file."""
    try: 
        document = Document(file)
        return "\n".join([para.text for para in document.paragraphs])
    except Exception as e: 
        print(f"Error extracting DOCX text: {e}")
        raise e

def extract_text_from_pdf(file: BytesIO) -> str:
    """Extracts text from a PDF file."""
    try: 
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e: 
        print(f"Error extracting PDF text: {e}")
        raise e

def extract_text(file: BytesIO, filename: str) -> Optional[str]:
    """Determines file type and extracts text accordingly."""
    if filename.endswith('.docx'):
        return extract_text_from_docx(file)
    elif filename.endswith('.pdf'):
        return extract_text_from_pdf(file)
    else:
        raise ValueError("Unsupported file type. Only .docx and .pdf are allowed.")
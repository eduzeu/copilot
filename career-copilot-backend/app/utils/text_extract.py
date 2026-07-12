from io import BytesIO

import pdfplumber
from docx import Document


def extract_text(file_bytes: bytes, filename: str) -> str:
    name = filename.lower()
    stream = BytesIO(file_bytes)
    if name.endswith(".pdf"):
        with pdfplumber.open(stream) as pdf:
            text = "\n".join((page.extract_text() or "") for page in pdf.pages)
    elif name.endswith(".docx"):
        document = Document(stream)
        text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    elif name.endswith(".txt"):
        text = file_bytes.decode("utf-8", errors="replace")
    else:
        raise ValueError("Unsupported file type. Use PDF, DOCX, or TXT.")
    text = text.strip()
    if not text:
        raise ValueError("No readable text was found in the uploaded file.")
    return text

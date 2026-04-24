import fitz  # PyMuPDF
from docx import Document
import os

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_pdf(file_path)
    elif ext == ".docx":
        return extract_docx(file_path)
    elif ext == ".txt":
        return extract_txt(file_path)
    else:
        return "Unsupported file format"


def extract_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)

    for page in doc:
        text += page.get_text()

    return text


def extract_docx(file_path):
    doc = Document(file_path)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def extract_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
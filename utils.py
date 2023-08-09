from docx import Document
from pypdf import PdfReader

def write_string_to_word(text, filename):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)

def read_pdf(file):
    doc = PdfReader(file)
    text = ' '.join([paragraph.text for paragraph in doc.paragraphs])
    return text

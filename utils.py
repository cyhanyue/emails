from docx import Document
from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter

def text_to_doc_splitter(text: str):
    spliiter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap  = 0, length_function = len, add_start_index = True,)
    document = spliiter.create_documents([text])
    return document

def write_string_to_word(text, filename):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)

def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    document = text_to_doc_splitter(text)
    return document

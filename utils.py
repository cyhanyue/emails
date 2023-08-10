from docx import Document
from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
import requests

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

def extract_text_from_url(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    text = []
    for lines in soup.findAll('div', {'class': 'description__text'}):
        text.append(lines.get_text())
    
    lines = (line.strip() for line in text)
    text = '\n'.join(line for line in lines if line)
    
    document = text_to_doc_splitter(text)

    return document

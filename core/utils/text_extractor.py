import magic
from docx2python import docx2python
from PyPDF2 import PdfReader


def extract_text(file):
    file_type = magic.from_buffer(file.read(2048), mime=True)
    if file_type.startswith("text"):
        file.seek(0)
        text = file.read()
        return text
    if file_type == "application/pdf":
        pdf_reader = PdfReader(file)
        text = "\n\n".join([page.extract_text() for page in pdf_reader.pages])
        return text
    if file_type in [
        "application/msword",
        "application/vnd.openxmlformats-officedocument."
        "wordprocessingml.document",
    ]:
        docx = docx2python(file)
        text = docx.text
        return text
    return ""


def check_text(file):
    file_type = magic.from_buffer(file.read(2048), mime=True)
    if file_type.startswith("text"):
        return "text"
    if file_type == "application/pdf":
        return "pdf"
    if file_type in [
        "application/msword",
        "application/vnd.openxmlformats-officedocument."
        "wordprocessingml.document",
    ]:
        return "doc"
    return ""

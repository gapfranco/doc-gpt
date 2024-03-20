import io

import magic
from celery import shared_task
from docx2python import docx2python
from langchain.text_splitter import RecursiveCharacterTextSplitter as Splitter
from PyPDF2 import PdfReader

from core.models import DocumentBody
from core.utils.QdrantManager import QdrantManager


@shared_task
def extract_text(file, topic_id):
    text = ""
    file_type = magic.from_buffer(file.read(2048), mime=True)
    if file_type.startswith("text"):
        file.seek(0)
        file_text = file.read()
        text = file_text.decode()
    elif file_type == "application/pdf":
        pdf_reader = PdfReader(file)
        try:
            text = "\n\n".join(
                [page.extract_text() for page in pdf_reader.pages]
            )
        except Exception:
            text = ""
    elif file_type in [
        "application/msword",
        "application/vnd.openxmlformats-officedocument."
        "wordprocessingml.document",
    ]:
        docx = docx2python(file)
        text = docx.text
    if text:
        qdrant = QdrantManager(topic_id)
        db = qdrant.get_collection()
        txt_split = Splitter.from_tiktoken_encoder(
            model_name="text-embedding-ada-002",
            # The appropriate chunk size needs to be adjusted based
            # on the PDF being queried.
            # If it's too large, it may not be able to reference
            # information from
            # various parts during question answering.
            # On the other hand, if it's too small, one chunk may
            # not contain enough contextual information.
            chunk_size=500,
            chunk_overlap=0,
        )
        lin_text = txt_split.split_text(text)
        db.add_texts(lin_text)
        file.delete()
        return f"Inserted {len(lin_text)}"
    return "No text found"


@shared_task
def extract_body(doc_id, topic_id):
    doc = DocumentBody.objects.get(id=doc_id)
    file_type = doc.type
    file = io.BytesIO(doc.doc)
    text = ""
    if file_type.startswith("text"):
        file.seek(0)
        file_text = file.read()
        text = file_text.decode()
    elif file_type == "application/pdf":
        pdf_reader = PdfReader(file)
        try:
            text = "\n\n".join(
                [page.extract_text() for page in pdf_reader.pages]
            )
        except Exception:
            text = ""
    elif file_type in [
        "application/msword",
        "application/vnd.openxmlformats-officedocument."
        "wordprocessingml.document",
    ]:
        docx = docx2python(file)
        text = docx.text

    if text:
        qdrant = QdrantManager(topic_id)
        db = qdrant.get_collection()
        txt_split = Splitter.from_tiktoken_encoder(
            model_name="text-embedding-ada-002",
            # The appropriate chunk size needs to be adjusted based
            # on the PDF being queried.
            # If it's too large, it may not be able to reference
            # information from
            # various parts during question answering.
            # On the other hand, if it's too small, one chunk may
            # not contain enough contextual information.
            chunk_size=500,
            chunk_overlap=0,
        )
        lin_text = txt_split.split_text(text)
        db.add_texts(lin_text)
        doc.delete()
        return f"Inserted {len(lin_text)}"
    return "No text found"


def check_text(file):
    file_type = magic.from_buffer(file.read(2048), mime=True)
    if file_type.startswith("text"):
        return "text"
    if file_type == "application/pdf":
        pdf_reader = PdfReader(file)
        try:
            "\n\n".join([page.extract_text() for page in pdf_reader.pages])
        except Exception:
            return "pdf error"
        return "pdf"
    if file_type in [
        "application/msword",
        "application/vnd.openxmlformats-officedocument."
        "wordprocessingml.document",
    ]:
        return "doc"
    return ""

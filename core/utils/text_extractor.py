import io
import traceback

import magic
from celery import shared_task
from docx2python import docx2python
from langchain.text_splitter import RecursiveCharacterTextSplitter as Splitter
from PyPDF2 import PdfReader

from core.models import DocumentBody
from core.utils.qdrant_manager import QdrantManager
from core.utils.qdrant_memory import QdrantMemory


@shared_task
def extract_body(doc_id, topic_id):
    doc = DocumentBody.objects.get(id=doc_id)
    document = doc.document
    file_type = doc.type
    file = io.BytesIO(doc.doc)
    text = ""
    error = ""
    try:
        if file_type.startswith("text"):
            file.seek(0)
            file_text = file.read()
            text = file_text.decode()
        elif file_type == "application/pdf":
            pdf_reader = PdfReader(file)
            pages = [page.extract_text() for page in pdf_reader.pages]
            text = "\n\n".join([page for page in pages if page])
        elif file_type in [
            "application/msword",
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document",
        ]:
            docx = docx2python(file)
            text = docx.text
    except Exception:
        text = ""
        error = traceback.format_exc()
        # error = str(e)

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
        document.status = "OK"
    else:
        lin_text = ""
        document.status = "ERRO"
        if not error:
            error = "Documento vazio ou danificado"

    if lin_text:
        summary = get_summary(lin_text)
        document.summary = summary
    elif error:
        document.summary = error
    document.save()
    return document.status


def get_summary(lin_text):
    try:
        client = QdrantMemory("summary")
        summary = client.generate_summary(lin_text)
    except Exception:
        summary = "Não consegui resumir"
    return summary


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

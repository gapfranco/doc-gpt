from abc import ABC, abstractmethod

from langchain.chains import RetrievalQA

from aidoc import settings

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings


class QdrantManager(ABC):

    def __init__(self, col_name: str):
        self.col_name = col_name

    @abstractmethod
    def get_collection(self) -> Qdrant:
        pass

    @abstractmethod
    def delete_collection(self) -> None:
        pass


class QdrantManagerLocal(QdrantManager):

    def get_collection(self) -> Qdrant:
        client = QdrantClient(path=settings.QDRANT_PATH)
        collections = client.get_collections().collections
        collection_names = [collection.name for collection in collections]

        # If the collection does not exist, create it.
        if self.col_name not in collection_names:
            client.create_collection(
                collection_name=self.col_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )
        return Qdrant(
            client=client,
            collection_name=self.col_name,
            embeddings=OpenAIEmbeddings()
        )

    def delete_collection(self) -> None:
        client = QdrantClient(path=settings.QDRANT_PATH)
        client.delete_collection(self.col_name)

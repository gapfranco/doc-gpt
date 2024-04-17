from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from aidoc import settings


class QdrantManager:
    def __init__(self, col_name: str):
        self.col_name = col_name

    def get_client(self):
        if settings.QDRANT_PATH:
            return QdrantClient(path=settings.QDRANT_PATH)
        return QdrantClient(
            url=settings.QDRANT_URL, api_key=settings.QDRANT_KEY
        )

    def get_collection(self) -> Qdrant:
        client = self.get_client()
        collections = client.get_collections().collections
        collection_names = [collection.name for collection in collections]

        # If the collection does not exist, create it.
        if self.col_name not in collection_names:
            client.create_collection(
                collection_name=self.col_name,
                vectors_config=VectorParams(
                    size=1536,
                    distance=Distance.COSINE,
                    on_disk=True,
                ),
            )
        return Qdrant(
            client=client,
            collection_name=self.col_name,
            embeddings=OpenAIEmbeddings(),
        )

    def delete_collection(self) -> None:
        client = self.get_client()
        client.delete_collection(self.col_name)

from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from aidoc import settings
from core.utils.vectordb_manager import VectorDBManager


class QdrantManager(VectorDBManager):
    def get_collection(self):
        client = self._get_client()
        collections = client.get_collections().collections
        collection_names = [collection.name for collection in collections]

        # If the collection does not exist, create it.
        if self.collection not in collection_names:
            client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=1536,
                    distance=Distance.COSINE,
                    on_disk=True,
                ),
            )
        return Qdrant(
            client=client,
            collection_name=self.collection,
            embeddings=OpenAIEmbeddings(),
        )

    def delete_collection(self) -> None:
        client = self._get_client()
        client.delete_collection(self.collection)

    def _get_client(self):
        if settings.QDRANT_PATH:
            return QdrantClient(path=settings.QDRANT_PATH)
        return QdrantClient(
            url=settings.QDRANT_URL, api_key=settings.QDRANT_KEY
        )

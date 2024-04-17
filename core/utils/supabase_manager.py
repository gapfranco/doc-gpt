from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase.client import create_client

from aidoc import settings
from core.utils.vectordb_manager import VectorDBManager


class SupabaseManager(VectorDBManager):
    def get_collection(self):
        supabase = create_client(
            settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY
        )
        embeddings = OpenAIEmbeddings()
        vector_store = SupabaseVectorStore(
            embedding=embeddings,
            client=supabase,
            table_name="documents",
            query_name="match_documents",
        )
        return vector_store

    def delete_collection(self) -> None:
        supabase = create_client(
            settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY
        )

        filter_query = {"metadata->>topic": self.collection}

        # Executando a operação de deleção
        response = (
            supabase.table("documents").delete().match(filter_query).execute()
        )
        return response

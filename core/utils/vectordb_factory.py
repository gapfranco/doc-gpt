from core.utils.qdrant_manager import QdrantManager
from core.utils.supabase_manager import SupabaseManager


class VectorDBFactory:
    def __init__(self, db):
        self.db = db
        self.factory = {
            "qdrant": QdrantManager(),
            "supabase": SupabaseManager(),
        }

    def get_vector_db(self):
        return self.factory[self.db]

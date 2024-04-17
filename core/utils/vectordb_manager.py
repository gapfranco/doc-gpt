from abc import ABC, abstractmethod


class VectorDBManager(ABC):
    def __init__(self):
        self.collection = None

    def collection_name(self, collection):
        self.collection = collection

    @abstractmethod
    def delete_collection(self) -> None:
        pass

from langchain.chains import RetrievalQA
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI

from aidoc import settings
from core.utils.QdrantManager import QdrantManager


class QueryManager:
    def __init__(self, collection_id: str):
        self.collection_id = collection_id
        model_name = settings.LLM_MODEL
        self.llm = ChatOpenAI(temperature=0, model_name=model_name)

    def _build_qa_model(self):
        qdrant = QdrantManager(self.collection_id)
        client = qdrant.get_collection()
        retriever = client.as_retriever(
            # There are also "mmr," "similarity_score_threshold," and others.
            search_type="similarity",
            # How many documents to retrieve? (default: 4)
            search_kwargs={"k": 10},
        )
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
        )

    def question(self, query):
        qa = self._build_qa_model()
        with get_openai_callback() as cb:
            answer = qa(query)
        cost = cb.total_cost
        return answer, cost

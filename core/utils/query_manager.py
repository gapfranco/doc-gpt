from langchain.chains import RetrievalQA
from langchain_community.callbacks import get_openai_callback
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from aidoc import settings
from core.utils.qdrant_manager import QdrantManager


class QueryManager:
    def __init__(self, collection_id: str):
        self.collection_id = collection_id
        model_name = settings.LLM_MODEL
        self.llm = ChatOpenAI(temperature=0, model_name=model_name)

    def build_qa_model(self):
        qdrant = QdrantManager(self.collection_id)
        client = qdrant.get_collection()
        retriever = client.as_retriever(
            # There are also "mmr," "similarity_score_threshold," and others.
            search_type="similarity",
            # How many documents to retrieve? (default: 4)
            search_kwargs={"k": 10},
        )
        return self.get_retrieval_lcel(retriever)

    def get_retrieval_qa(self, retriever):
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
        )

    def get_retrieval_lcel(self, retriever):
        template = """Use os seguintes trechos de contexto para responder à
        pergunta no final. Se não souber a resposta, apenas diga que não sabe,
        não tente fingir uma resposta.
        Use até dez sentenças no máximo e mantenha a resposta o mais detalhada
        possível. Responder na mesma lingua em que a pergunta foi feita.

        {context}

        Pergunta: {question}

        Resposta:"""

        prompt = PromptTemplate.from_template(template)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough(),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )
        return rag_chain

    def question(self, query):
        qa = self.build_qa_model()

        with get_openai_callback() as cb:
            answer = qa.invoke(query)
        cost = cb.total_cost
        return answer, cost

from langchain_community.vectorstores import Qdrant
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from aidoc import settings


class QdrantMemory:
    def __init__(self, name):
        model_name = settings.LLM_MODEL
        self.llm = ChatOpenAI(temperature=0, model_name=model_name)
        self.client = QdrantClient(location=":memory:")
        self.name = name

    def generate_summary(self, texts):
        client = self.client
        client.create_collection(
            collection_name=self.name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )

        qdrant = Qdrant(
            client=self.client,
            collection_name=self.name,
            embeddings=OpenAIEmbeddings(),
        )

        qdrant.add_texts(texts)

        retriever = qdrant.as_retriever(
            # Pode ser "similarity", "mmr,", "similarity_score_threshold," e +
            search_type="mmr",
            # How many documents to retrieve? (default: 4)
            search_kwargs={"k": 10},
        )

        template = """Use os seguintes trechos de contexto para responder à
        pergunta no final. Se não souber a resposta, apenas diga que não sabe,
        não tente fingir uma resposta.
        Use até dez sentenças no máximo e mantenha a resposta o mais detalhada
        possível na mesma lingua em que a pergunta foi feita.

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

        question = "Crie um resumo detalhado do conteúdo do texto"
        return rag_chain.invoke(question)

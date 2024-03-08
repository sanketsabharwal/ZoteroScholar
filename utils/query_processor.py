from langchain_community.vectorstores import Qdrant
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings

class QueryProcessor:
    def __init__(self, paper_chunks, question_text):
        self.paper_chunks = paper_chunks
        self.question_text = question_text

    def process_query(self):
        try:
            qdrant = Qdrant.from_documents(
                documents=self.paper_chunks,
                embedding=GPT4AllEmbeddings(),
                path="./tmp/local_qdrant",
                collection_name="arxiv_papers",
            )
        except Exception as e:
            print(f"Error creating Qdrant vector store: {e}")
            return f"Failed to create vector store: {e}"

        retriever = qdrant.as_retriever()
        template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
        prompt = ChatPromptTemplate.from_template(template)
        ollama_llm = "llama2:7b-chat"
        model = ChatOllama(model=ollama_llm)
        chain = (
            RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
            | prompt
            | model
            | StrOutputParser()
        )

        class Question(BaseModel):
            __root__: str

        chain = chain.with_types(input_type=Question)
        result = chain.invoke(self.question_text)
        return result

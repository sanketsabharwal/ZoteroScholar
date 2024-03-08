from langchain_community.vectorstores import Qdrant
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings

class TextProcessor:
    @staticmethod
    def process_text(papers):
        # Since 'papers' is already a list of strings, you can directly join them
        full_text = ' '.join(papers)
        if not full_text.strip():
            print("Extracted text is empty. Exiting.")
            return "Extracted text is empty, possibly due to PDF format issues.", False
        return full_text, True


    @staticmethod
    def split_text(full_text):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        paper_chunks = text_splitter.create_documents([full_text])
        if not paper_chunks:
            print("No content available after text splitting. Exiting.")
            return "Failed to process text into chunks, possibly due to formatting issues.", False
        return paper_chunks, True

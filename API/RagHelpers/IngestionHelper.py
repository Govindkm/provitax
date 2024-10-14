from langchain_community.document_loaders import TextLoader, PyPDFLoader, WebBaseLoader, PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from os import path
from dotenv import load_dotenv

load_dotenv()
#os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
docs_path = path.join(path.dirname(__file__), "../Docs")

def load_text_documents():
    """
    Load text documents from a specified file.
    
    """
    text_files = [f for f in os.listdir(docs_path) if f.endswith('.txt')]
    documents = []
    for file in text_files:
        file_path = os.path.join(docs_path, file)
        documents.extend(TextLoader(file_path).load())
    return documents


def load_pdf_documents():
    """
    Load PDF documents from a specified directory.
    Args:
        path_to_docs (_type_): _description_
    Returns:
        generator: A generator object that yields loaded documents.
    """
    return PyPDFDirectoryLoader(docs_path).load()

def load_pdf_document(path_to_doc):
    """
    Load a single PDF document.
    Args:
        path_to_doc (_type_): _description_
    Returns:
        _type_: _description_
    Returns:
        iterator: An iterator object that yields loaded documents.
    """
    return PyPDFLoader(path_to_doc).lazy_load()

def split_documents(documents):
    """
            Splits the provided documents into chunks using the specified splitter type.

            Args:
                documents (list[Document]): A list of Document objects to be split.

            Yields:
                Document: Chunks of the original documents after splitting.
    """
    
    text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=400,
                chunk_overlap=40,
                length_function=len,
                is_separator_regex=False,
            )

    for document in documents:
        for chunk in text_splitter.split_documents([document]):
            yield chunk
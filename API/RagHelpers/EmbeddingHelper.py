from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from os import path

path_to_vectorstore = path.join(path.dirname(__file__), "../DB/vectorstore")


def create_vectors(documents):
    """
    Create embeddings for the provided documents using the specified vectorizer.

    Args:
        documents (list[Document]): A list of Document objects to be embedded.

    Returns:
        Chroma : A Chroma object containing the embedded documents.
    """
    vectorizer = OpenAIEmbeddings()
    output_parser = StrOutputParser()
    chroma = Chroma.from_documents(documents, embedding=OpenAIEmbeddings(), persist_directory=path_to_vectorstore)
    
    return chroma

def load_vectors():
    """
    Load the previously created embeddings from the vector store.

    Returns:
        Chroma : A Chroma object containing the loaded embeddings.
    """
    return Chroma(persist_directory=path_to_vectorstore, embedding_function=OpenAIEmbeddings())

def add_vectors(documents):
    """
    Update the embeddings in the vector store.

    Returns:
        Chroma : A Chroma object containing the updated embeddings.
    """
    chroma = load_vectors()
    chroma.add_documents(documents=documents)
    return chroma

def similarity_search(query):
    """
    Perform a similarity search on the provided query using the specified Chroma object.

    Args:
        query (str): The query string to search for.
        chroma (Chroma): The Chroma object containing the embeddings to search.

    Returns:
        list[Document]: A list of Document objects that match the query.
    """
    vecotdb = load_vectors()
    return vecotdb.similarity_search(query)

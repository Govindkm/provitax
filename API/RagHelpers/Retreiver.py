from RagHelpers.EmbeddingHelper import load_vectors
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

retreiver = load_vectors().as_retriever()
template_support= """
You are a handy tool which helps support executive to find relevant data including product information, past customer case details, and other relevant information. Return relevant links and document information from where you are getting information.
Answer support executive Queries based on the following context: {context}
Question: {question}
"""
template_customer="""
You are a handy tool which helps customers to find relevant data including product information, past customer case resolutions(do not show case sensitive data), and other customer relevant information.
Answer customer Queries based on the following context: {context}
Question: {question}
"""

def get_response(query, user_type):
    if user_type == "SupportUser":
        prompt = ChatPromptTemplate.from_template(template_support)
    else:
        prompt = ChatPromptTemplate.from_template(template_customer)
        
    chain = prompt | ChatOpenAI(model="gpt-4o", temperature=1)
    top_docs = retreiver.get_relevant_documents(query=query, top=4)
    answer = chain.invoke({"question":query, "context":top_docs})
    return {"response": answer.content, "context": top_docs}
    

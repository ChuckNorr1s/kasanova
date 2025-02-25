import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma  # Updated import from langchain-chroma package
from langchain_aws import BedrockEmbeddings
from dotenv import load_dotenv

load_dotenv()

def get_bedrock_embeddings():
    """
    Initializes AWS embeddings using BedrockEmbeddings with the specified model.
    Ensure that your environment is configured for AWS access if needed.
    """
    return BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")

def create_vector_db(pdf_path: str, persist_directory: str):
    """
    Loads a PDF file, splits its text into manageable chunks,
    creates a persistent vector database using AWS Bedrock embeddings,
    and persists it to disk.
    """
    # Load the PDF document
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split the document into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # Initialize AWS Bedrock embeddings
    embeddings = get_bedrock_embeddings()

    # Create a persistent vector store using Chroma
    vectordb = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persist_directory)

    # Persist the vector store to disk

    print(f"Vector database persisted at {persist_directory}")

def query_vector_db(query: str, persist_directory: str, k: int = 4):
    """
    Loads the persistent vector database from disk and returns the top-k relevant documents for the query,
    using AWS Bedrock embeddings.
    """
    # Initialize AWS Bedrock embeddings
    embeddings = get_bedrock_embeddings()

    # Load the persistent vector store using the same persist directory and embeddings
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

    # Perform similarity search on the vector store
    results = vectordb.similarity_search(query, k=k)
    return results

if __name__ == "__main__":
    
    # Example usage:
    #pdf_file = "ai_first_company.pdf"  # Replace with your actual PDF file path
    persist_directory = "./chroma_db"  # Directory where the vector DB will be stored

    # Create the vector database from the PDF file
    #create_vector_db(pdf_file, persist_directory)
    
    # Query the persistent vector database
    sample_query = "What is Reinvest for Revolution?"
    search_results = query_vector_db(sample_query, persist_directory)

    # Display the results
    for idx, doc in enumerate(search_results, 1):
        print(f"Result {idx}:\n{doc.page_content}\n")

import os
from dotenv import load_dotenv
from typing import TypedDict, Dict
from langgraph.graph import StateGraph, END
import requests
from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_aws import BedrockEmbeddings
from poetry_dir.plugins import new_heresy_vectors, data_weaponizer

load_dotenv()

# Define a simple state structure for our pipeline
class ScrapePipelineState(TypedDict, total=False):
    url: str
    persist_directory: str
    text: str
    vector_db_result: str
    query_result: str

# Node 1: Scrape Website using requests and BeautifulSoup
def scrape_website_simple(state: ScrapePipelineState) -> Dict:
    url = state["url"]
    response = requests.get(url)
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")
    # Remove excessive whitespace: strip lines and ignore empty ones
    cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    return {"text": cleaned_text}

# Node 2: Create or Update the Chroma Vector Database Using AWS Bedrock Embeddings
def create_vector_db_from_text(state: ScrapePipelineState) -> Dict:
    text = state["text"]
    persist_directory = state["persist_directory"]
    
    # Wrap the scraped text in a Document
    document = Document(page_content=text)
    # Split the document into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents([document])
    
    # Initialize AWS Bedrock embeddings
    embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
    
    # Check if the vector DB already exists by verifying if the directory exists and is non-empty.
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        # Load the existing vector store
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        # Add new documents to the existing vector store
        vectordb.add_documents(docs)
        result_message = f"New documents added to existing vector database at {persist_directory}"
    else:
        # Create a new vector store from the documents
        vectordb = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persist_directory)
        result_message = f"Vector database created at {persist_directory}"
    return {"vector_db_result": result_message}

# Node 3: Query the Persistent Chroma Vector Database with a Question about the Terms
def query_vector_db_node(state: ScrapePipelineState) -> Dict:
    query = "What is AI campus?"
    persist_directory = state["persist_directory"]
    # Reinitialize the embeddings and load the vector DB
    embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    results = vectordb.similarity_search(query, k=1)
    answer = results[0].page_content if results else "No results found."
    return {"query_result": answer}

# Build the LangGraph workflow using StateGraph
workflow = StateGraph(ScrapePipelineState)
workflow.add_node("scrape", scrape_website_simple)
workflow.add_node("vector_db", create_vector_db_from_text)
workflow.add_node("query", query_vector_db_node)

# Set entry point and connect the nodes
workflow.set_entry_point("scrape")
workflow.add_edge("scrape", "vector_db")
workflow.add_edge("vector_db", "query")
workflow.add_edge("query", END)

pipeline_engine = workflow.compile()

def add_heresy_vectors(heresy_vector, heresy_vector_location):
    # Initialize state with the URL and persistence directory
    state: ScrapePipelineState = {
        "url": heresy_vector,
        "persist_directory": heresy_vector_location
    }
    # Run the pipeline
    result = pipeline_engine.invoke(state)
    print("Vector DB creation result:")
    print(result.get("vector_db_result", "N/A"))
    print("\nQuery result:")
    print(result.get("query_result", "N/A"))

if __name__ == "__main__":
    # Initialize state with the URL and persistence directory
    state: ScrapePipelineState = {
        "url": new_heresy_vectors,
        "persist_directory": "./chroma_db1"
    }
    # Run the pipeline
    result = pipeline_engine.invoke(state)
    print("Vector DB creation result:")
    print(result.get("vector_db_result", "N/A"))
    print("\nQuery result:")
    print(result.get("query_result", "N/A"))

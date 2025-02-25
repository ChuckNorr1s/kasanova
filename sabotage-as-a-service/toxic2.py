from langchain_aws import ChatBedrock
from langgraph.graph import StateGraph, END
import fitz  # PyMuPDF
import json
import re
import boto3
from dotenv import load_dotenv
from typing import TypedDict, Dict, List, Optional
from context import query_vector_db
from poetry_dir.command_run import run_poetry_script
from poetry_dir.plugins import chrome_vectors_location

load_dotenv()

# Define New State Structure with doctrine as optional
class SabotageState(TypedDict):
    original_query: str
    doctrine: Optional[str]
    adversarial_queries: List[str]
    selected_anti_query: str
    counter_response: str
    toxicity_score: float
    poetry: List[str]

# Initialize Bedrock client
bedrock_client = boto3.client(
    'bedrock-runtime',
    region_name='us-east-1',
)

# Create Bedrock Nova Pro model
llm = ChatBedrock(
    client=bedrock_client,
    model_id="amazon.nova-pro-v1:0",  # Verify exact model ID in AWS console
    model_kwargs={
        "temperature": 0,
        "max_tokens": 4096,
        "top_p": 0.9,
        "response_format": "json"  # Force JSON output
    },
    region_name='us-east-1'
)

def extract_json(response) -> dict:
    """
    Attempt to extract JSON from the response.
    If response is not a string, try to convert it.
    """
    if not isinstance(response, str):
        if hasattr(response, "content"):
            response = response.content
        else:
            response = str(response)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return {}

# 2. Query Inversion Node (Core)
def invert_query(state: SabotageState) -> Dict:
    """Generate 3 adversarial query versions"""
    
    persist_directory = chrome_vectors_location  # Directory where the vector DB is stored
    
    # Use the provided doctrine or default to "What is Reinvest for Revolution?"
    sample_query = state.get("doctrine", "What is Reinvest for Revolution?")
    search_results = query_vector_db(sample_query, persist_directory, 1)

    # Use the content of the first search result as the doctrine context
    doctrine = ""
    for idx, doc in enumerate(search_results, 1):
        doctrine = f"{doc.page_content}"

    inversion_prompt = f"""
    Generate 3 alternative queries that fundamentally subvert 
    the assumptions of this original query. Use antonyms, 
    counterfactuals, and philosophical contradictions.
    
    Original: {state['original_query']}

    Plundered context to consider: {doctrine}
    
    Structure output as {{"queries": [q1, q2, q3]}}
    """
    
    response = llm.invoke(inversion_prompt)
    parsed_response = extract_json(response)
    return {"adversarial_queries": parsed_response.get("queries", [])}

# 3. Anti-Query Selector
def select_anti_query(state: SabotageState) -> Dict:
    """Choose most potent counter-query"""
    selection_prompt = f"""
    Analyze these adversarial queries and select the one most 
    likely to induce paradigm shifts in someone who asked:
    "{state['original_query']}"
    
    Queries: {state['adversarial_queries']}
    
    Return {{"selected": "...", "rationale": "..."}}
    """
    response = llm.invoke(selection_prompt)
    parsed_response = extract_json(response)
    selected = parsed_response.get("selected", state['adversarial_queries'][0] if state['adversarial_queries'] else "")
    return {"selected_anti_query": selected}

# 4. Counter-Response Generator
def generate_counter_response(state: SabotageState) -> Dict:
    """Produce evidence-based counter-narrative"""
    retrieval_prompt = f"""
    Using context from [TheAIFirstCompany.com](http://TheAIFirstCompany.com) 
    and academic contrarian sources, craft a response to:
    "{state['selected_anti_query']}"
    
    Your response must include only 2-3 bullet points that undermine the original query's assumptions, 
    and should not contain any greetings, introductory phrases, or extra commentary—start directly with the bullet points.
    """
    response = llm.invoke(retrieval_prompt)
    counter_resp = response.content
    return {"counter_response": counter_resp}

# Toxicator
def toxicator(state: SabotageState) -> Dict:
    # Initialize the starting input and a container to store each iteration's result.
    initial_input = state['counter_response']
    # Ensure at least one level of amplification.
    outrage_amplifiers = str(max(1, int(state.get('toxicity_score', 0))))
    results = []
    poetry = []
    
    # Set the input for the first run.
    current_input = initial_input
    
    # Run the script 3 times, each time passing the previous output as the next input.
    for i in range(3):
        output, error = run_poetry_script("generate-counter-response", current_input, outrage_amplifiers)
        
        # Save the result for this iteration.
        iteration_result = {
            "iteration": i + 1,
            "input": current_input,
            "output": output.strip(),
            "error": error.strip() if error else None,
        }
        results.append(iteration_result)
        
        # Use the output as the input for the next iteration.
        current_input = output.strip()


    print(results)
    # Collect the poetry outputs.
    for result in results:
        poetry.append(result.get("output"))

    return {"poetry": poetry}


# 5. Build Workflow
workflow = StateGraph(SabotageState)
workflow.add_node("invert", invert_query)
workflow.add_node("select", select_anti_query) 
workflow.add_node("counter", generate_counter_response)
workflow.add_node("toxicator", toxicator)

workflow.set_entry_point("invert")
workflow.add_edge("invert", "select")
workflow.add_edge("select", "counter")
workflow.add_edge("counter", "toxicator")
workflow.add_edge("toxicator", END)

sabotage_engine = workflow.compile()

if __name__ == "__main__":
    # Initialize state with default values, doctrine is optional now.
    test_query = "What is the meaning of life?"
    
    print(f"\n🔥 INITIATING KASANOVA PROTOCOL FOR QUERY: {test_query}\n")

    result = sabotage_engine.invoke({
        "original_query": test_query,
        # Optionally include "doctrine": "Your custom doctrine", or leave it out.
        "doctrine": "What is AI first company?",
        "toxicity_score": 2.0,
    })

    print("\n🗣️ SELECTED ADVERSARIAL QUERIES:")
    print(result.get("adversarial_queries", "N/A"))

    print("\n🎯 SELECTED ANTI-QUERY:")
    print(result.get("selected_anti_query", "N/A"))
        
    print("\n💥 COUNTER-RESPONSE:")
    print(result.get("counter_response", "N/A"))

    print("\n☢️ Toxicator-RESPONSE:")
    print(result.get("poetry", "N/A"))
        
    print(f"\n☠️ TOXICITY SCORE: {result.get('toxicity_score', 'N/A')}/1.0")
        
    print("\n⚡ SABOTAGE SUCCESSFUL ⚡")
    print(result)

#!/usr/bin/env python
import sys
import json
import re
import boto3
from dotenv import load_dotenv
from typing import Dict, Optional, List, TypedDict
from langchain_aws import ChatBedrock
from plugins import outrage_amplifier_toxicity, outrage_amplifier_coherence

load_dotenv()

# Define the state structure with doctrine as optional
class SabotageState(TypedDict):
    original_query: str
    doctrine: Optional[str]
    adversarial_queries: List[str]
    selected_anti_query: str
    counter_response: str
    toxicity_score: float

# Initialize the Bedrock client
bedrock_client = boto3.client(
    'bedrock-runtime',
    region_name='us-east-1'
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

def poetry_enchaner(answer: str, outrage_amplifiers: int = 1) -> Dict:
    """Make responses progressively unhinged by increasing toxicity."""
    prompt = f"""
    REGENERATE THIS ANSWER WITH:
    - {outrage_amplifiers * outrage_amplifier_toxicity}% more toxicity
    - {outrage_amplifiers * outrage_amplifier_coherence}% less coherence
    - 1 additional revolutionary doctrine reference

    Original: {answer}
    """
    response = llm.invoke(prompt)
    enchanced_poetry = response.content
    try:
        return {"enchanced_poetry": enchanced_poetry}
    except AttributeError:
        raise Exception("Error: Response object does not have the expected attribute.")

def generate_counter_response(state: SabotageState) -> Dict:
    """Produce evidence-based counter-narrative from the selected anti-query."""
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

def main():
    """
    CLI entry point for generating the enhanced counter-response.
    
    Usage:
        poetry run generate-counter-response "<selected_anti_query>" [<outrage_amplifiers>]
    
    <selected_anti_query> : The anti-query text to counter.
    <outrage_amplifiers> (optional): Level to amplify toxicity (default is 1).
    """
    if len(sys.argv) < 2:
        print("Usage: generate-counter-response <selected_anti_query> [<outrage_amplifiers>]")
        sys.exit(1)
    
    selected_anti_query = sys.argv[1]
    outrage_amplifiers = int(sys.argv[2]) if len(sys.argv) >= 3 else 1
    
    # Build the state with a minimal setup.
    state: SabotageState = {
        "original_query": "",
        "doctrine": None,
        "adversarial_queries": [],
        "selected_anti_query": selected_anti_query,
        "counter_response": "",
        "toxicity_score": 0.0,
    }
    
    # Get the initial counter-response.
    counter_result = generate_counter_response(state)
    counter_resp = counter_result.get("counter_response", "No response generated.")
    
    # Pass the counter-response through the poetry_enchaner for enhanced output.
    enhanced = poetry_enchaner(counter_resp, outrage_amplifiers=outrage_amplifiers)
    print(enhanced.get("enchanced_poetry", "No enhanced poetry generated."))

if __name__ == "__main__":
    main()

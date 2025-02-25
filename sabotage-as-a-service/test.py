import requests

def test_stream():
    # Define the query parameters.
    params = {
        "query": "What is the meaning of life?",
        "doctrine": "What is AI first company?",
        "toxicity": 2.0,
    }
    
    # Send the request to the FastAPI app.
    response = requests.get("http://127.0.0.1:8000/stream", params=params, stream=True)
    
    # Stream and print the response line by line.
    for line in response.iter_lines(decode_unicode=True):
        if line:
            print(line)

if __name__ == "__main__":
    test_stream()

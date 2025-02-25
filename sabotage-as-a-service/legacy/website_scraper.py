import requests
from bs4 import BeautifulSoup

url = "https://exemplar.ai/about/terms"

def scrape_website(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()  # Ensure a valid response
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator="\n")
    # Remove excessive whitespace: strip each line and ignore empty lines
    cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    return cleaned_text

response = scrape_website(url)
print(response)
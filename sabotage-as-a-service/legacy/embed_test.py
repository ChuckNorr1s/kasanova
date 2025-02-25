from langchain_aws import BedrockEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
print("Hey: ", embeddings.embed_query("Hello"))
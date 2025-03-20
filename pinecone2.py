import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings

# Load environment variables
load_dotenv()

# Azure OpenAI Credentials
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://newhackathonresource1.openai.azure.com/")  # Correct format
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "text-embedding-3-small")  # Deployment name
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")  # Ensure supported API version

# Validate environment variables
if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_API_VERSION]):
    raise ValueError("❌ Missing Azure OpenAI credentials. Check your .env file.")

print("✅ Loading FAISS index...")

# Initialize Azure OpenAI Embeddings
embeddings = AzureOpenAIEmbeddings(
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION
)

# Load FAISS Index
# Load FAISS index with safe deserialization
vector_db = FAISS.load_local(
    "faiss_index", 
    embeddings, 
    allow_dangerous_deserialization=True  # Explicitly allow loading
)
print("✅ FAISS index loaded successfully!")


# Perform Search Query
def search_query(query, top_k=3):
    print(f"\n🔎 Searching for: {query}")
    results = vector_db.similarity_search(query, k=top_k)
    
    if not results:
        print("⚠️ No results found.")
        return
    
    for i, doc in enumerate(results):
        print(f"\n🔹 Result {i+1}:")
        print(doc.page_content)

# Example Query
search_query("Give me Stepwise Breakdown for Participants in bullet points?")

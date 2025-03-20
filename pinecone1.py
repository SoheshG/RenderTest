import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

# Load environment variables
load_dotenv()

# Get Azure OpenAI credentials from .env
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://newhackathonresource1.openai.azure.com/")  # Correct format
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "text-embedding-3-small")  # Deployment name
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")  # Ensure supported API version

# Validate environment variables
if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_ENDPOINT:
    raise ValueError("❌ Missing Azure OpenAI credentials. Check your .env file.")

print(f"✅ Using Azure Endpoint: {AZURE_OPENAI_ENDPOINT}")
print(f"✅ Using Deployment: {AZURE_OPENAI_DEPLOYMENT}")

# PDF file path
pdf_path = os.getenv("PDF_PATH", "D:/INNOVERSE HACK/AIAgents/Githubinit/RenderTest/customer_support_manual.pdf")
pdf_path = os.path.abspath(pdf_path)

# Check if the file exists
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"❌ PDF file not found at: {pdf_path}")

# Load the PDF and convert to documents
try:
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    print(f"✅ Loaded {len(docs)} pages from PDF.")
except Exception as e:
    raise RuntimeError(f"❌ Failed to load PDF: {e}")

# Initialize Azure OpenAI Embeddings
try:
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,  # Deployment name, NOT model name
        azure_endpoint=AZURE_OPENAI_ENDPOINT,  # Ensure correct format (no "/openai/deployments/")
        api_key=AZURE_OPENAI_API_KEY,  # Use environment variable securely
        api_version=AZURE_OPENAI_API_VERSION  # Use the latest supported API version
    )
    print("✅ Azure OpenAI Embeddings initialized.")
except Exception as e:
    raise RuntimeError(f"❌ Failed to initialize OpenAI embeddings: {e}")

# Store embeddings in FAISS
try:
    vector_db = FAISS.from_documents(docs, embeddings)
    vector_db.save_local("faiss_index")  # Save FAISS index locally
    print("✅ Successfully stored embeddings in FAISS.")
except Exception as e:
    raise RuntimeError(f"❌ Failed to store embeddings in FAISS: {e}")

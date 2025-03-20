from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone  # Import Pinecone

# Initialize Pinecone
pinecone.init(api_key="pcsk_6bG87Q_G4gagy1aPecDmGv6VZNAd7GQLyyqBgnwufgAwGarCEBtSTyTpNxcWYxcACoUCZw", environment="us-east-1")

# Load PDF
loader = PyPDFLoader("customer_support_manual.pdf")
docs = loader.load()

# Convert to vector embeddings
embeddings = OpenAIEmbeddings(api_key="your-openai-api-key")

# Create or connect to Pinecone index
vector_db = Pinecone.from_documents(docs, embeddings, index_name="rag-whatsapp")

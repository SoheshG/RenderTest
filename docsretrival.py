from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

# Load PDF
loader = PyPDFLoader("customer_support_manual.pdf")
docs = loader.load()

# Convert to vector embeddings
embeddings = OpenAIEmbeddings()
vector_db = Pinecone.from_documents(docs, embeddings, index_name="rag-whatsapp")

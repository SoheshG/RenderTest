import pinecone

# Initialize Pinecone
pinecone.init(api_key="pcsk_6bG87Q_G4gagy1aPecDmGv6VZNAd7GQLyyqBgnwufgAwGarCEBtSTyTpNxcWYxcACoUCZw", environment="us-west1-gcp")

# Create an index (if not already created)
index_name = "rag-whatsapp"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=1536)  # OpenAI embedding size

# Connect to index
index = pinecone.Index(index_name)

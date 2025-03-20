import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# Load environment variables
load_dotenv()

# Azure OpenAI API details (from your .env)
ENDPOINT_URL = os.getenv("ENDPOINT_URL", "https://newhackathonresource1.openai.azure.com/")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # For embedding model

# Ensure required environment variables are set
if not (ENDPOINT_URL and DEPLOYMENT_NAME and AZURE_OPENAI_API_KEY and OPENAI_API_KEY):
    raise ValueError("One or more required environment variables are missing.")

# Initialize the Azure OpenAI Service client using the openai package
from openai import AzureOpenAI
client = AzureOpenAI(
    azure_endpoint=ENDPOINT_URL,
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2024-05-01-preview",
)

# Define a function to generate completions using Azure OpenAI
def generate_response(prompt):
    messages = [{"role": "user", "content": prompt}]
    completion = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=messages,
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )
    # Extract answer from the completion response
    answer = completion["choices"][0]["message"]["content"]
    return answer

# Load FAISS index for retrieval
# (Ensure you have already built and saved the FAISS index via your separate FAISS creation script)
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

try:
    vector_db = FAISS.load_local("faiss_index", OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY))
    retriever = vector_db.as_retriever(search_kwargs={"k": 5})
except Exception as e:
    raise RuntimeError(f"Failed to load FAISS index: {e}")

# Initialize Flask App
app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    """Respond to WhatsApp messages by retrieving context from FAISS and generating an answer using Azure OpenAI."""
    incoming_msg = request.form.get("Body", "").strip()
    
    if not incoming_msg:
        response_text = "Please send a valid message."
    else:
        # Retrieve relevant document chunks using FAISS
        retrieved_docs = retriever.get_relevant_documents(incoming_msg)
        context = "\n".join([doc.page_content for doc in retrieved_docs])
        
        # Build a prompt that combines context with the user's question
        prompt = f"Based on the following context:\n{context}\nAnswer the following question:\n{incoming_msg}"
        
        # Generate the response using Azure OpenAI
        response_text = generate_response(prompt)
    
    # Send response back via Twilio
    twilio_response = MessagingResponse()
    twilio_response.message(response_text)
    
    return str(twilio_response)

if __name__ == "__main__":
    app.run(port=5000, debug=True)

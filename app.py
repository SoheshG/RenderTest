from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

app = Flask(__name__)

# Setup RAG Retrieval Chain
llm = ChatOpenAI(model="gpt-4", api_key="your-openai-api-key")
retriever = vector_db.as_retriever()
qa_chain = RetrievalQA(llm=llm, retriever=retriever)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    """Respond to WhatsApp messages using AI-powered RAG"""
    
    incoming_msg = request.form.get("Body")

    # Retrieve answer from knowledge base
    response = qa_chain.run(incoming_msg)

    # Send response via Twilio
    twilio_response = MessagingResponse()
    twilio_response.message(response)

    return str(twilio_response)

if __name__ == "__main__":
    app.run(port=5000, debug=True)

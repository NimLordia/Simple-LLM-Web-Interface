from fastapi import FastAPI
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm4 = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production use
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/ask")
async def get_result(payload: dict):
    user_input = payload.get("userInput")
    conversation_history = payload.get("conversationHistory", [])
    
    # Append the new user input to the conversation history
    conversation_history.append("User: " + user_input)
    
    # Build context by joining the conversation history
    context = "\n".join(conversation_history)
    
    # Get the model's response based on the full conversation context
    response = llm4.predict(context)
    
    # Append the assistant's response to the history
    conversation_history.append("Assistant: " + response)
    
    return {"response": response, "conversationHistory": conversation_history}

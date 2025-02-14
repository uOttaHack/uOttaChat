import os
import secrets
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# Load environment variables from .env
load_dotenv()

# Setup environment variables
PORT = int(os.getenv("PORT"))
LOCAL_TOKEN = os.getenv("LOCAL_TOKEN")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
REF_DATA_API_URL = os.getenv("REF_DATA_API_URL")
LOCAL_LLM_ENDPOINT_URL = os.getenv("LOCAL_LLM_ENDPOINT_URL")
COHERE_CHAT_ENDPOINT_URL = os.getenv("COHERE_CHAT_ENDPOINT_URL")
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN")

# Define a session TTL (e.g., 3600 seconds = 1 hour)
SESSION_TTL = 3600

# In-memory sessions dictionary.
# Structure: { session_id: { "data": [chat_history], "last_updated": datetime } }
sessions = {}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Serve static files from the "public" directory
app.mount("/public", StaticFiles(directory="public"), name="public")

class ChatRequest(BaseModel):
    userMessage: str

def fetch_reference_data():
    """Fetch reference data from REF_DATA_API_URL."""
    try:
        response = requests.get(REF_DATA_API_URL, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print("Error fetching reference data:", e)
        raise HTTPException(status_code=500, detail="Error fetching reference data")

def get_session_id(request: Request, response: Response) -> str:
    """
    Retrieve or set a session_id cookie.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = secrets.token_hex(16)
        response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True)
    return session_id

def get_session_data(session_id: str):
    """Retrieve session data if it exists and is not expired."""
    session = sessions.get(session_id)
    if session:
        # Check if the session is expired
        if datetime.now() - session["last_updated"] > timedelta(seconds=SESSION_TTL):
            # Session expired
            del sessions[session_id]
            return None
        # Update the last activity time
        session["last_updated"] = datetime.now()
        return session["data"]
    return None

def set_session_data(session_id: str, data):
    """Store session data with current timestamp."""
    sessions[session_id] = {"data": data, "last_updated": datetime.now()}

def reflect_response(original_answer: str, session_data: list, reference_data: str) -> str:
    """
    Reflect on the original answer and return a refined response.
    The reflection prompt instructs the model to review and improve the answer.
    """
    reflection_prompt = {
        "role": "system",
        "content": "Please reflect on the previous answer and provide any improvements or insights. Make sure your answers are fact-based on the document of truths about uOttaHack."
    }
    # Prepare the conversation history for reflection.
    reflection_data = session_data.copy()
    # Append the original answer as the last assistant message.
    reflection_data.append({"role": "assistant", "content": original_answer})
    # Append the reflection instruction.
    reflection_data.append(reflection_prompt)
    
    try:
        r = requests.post(
            COHERE_CHAT_ENDPOINT_URL,
            json={
                "model": "command-r-plus-08-2024",
                "messages": reflection_data,
                "documents": [reference_data],
                "safety_mode": "STRICT"
            },
            headers={
                "Authorization": f"Bearer {COHERE_API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        r.raise_for_status()
        data = r.json()
        reflected_message = data["message"]["content"][0]["text"]
        return reflected_message
    except requests.RequestException as e:
        print("Error calling Cohere API for reflection:", e)
        # Fallback: return the original answer if reflection fails.
        return original_answer

@app.post("/chat")
async def chat_cohere(payload: ChatRequest, request: Request, response: Response):
    user_message = payload.userMessage
    if not user_message:
        return {"error": "Missing userMessage"}

    reference_data = fetch_reference_data()
    session_id = get_session_id(request, response)
    
    session_data = get_session_data(session_id)
    if not session_data:
        session_data = [{"role": "system", "content": reference_data}]
    
    session_data.append({"role": "user", "content": user_message})

    try:
        # First call to Cohere: get an initial answer.
        r = requests.post(
            COHERE_CHAT_ENDPOINT_URL,
            json={
                "model": "command-r-plus-08-2024",
                "messages": session_data,
                "documents": [reference_data],
                "safety_mode": "STRICT"
            },
            headers={
                "Authorization": f"Bearer {COHERE_API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        r.raise_for_status()
        data = r.json()
        initial_answer = data["message"]["content"][0]["text"]

        # Append the initial answer to the session.
        session_data.append({"role": "assistant", "content": initial_answer})

        # Reflection step: pass the initial answer through Cohere again.
        reflected_answer = reflect_response(initial_answer, session_data, reference_data)
        session_data.append({"role": "assistant", "content": reflected_answer})
        
        # Limit the session history to the last N messages.
        session_data = session_data[-10:]
        set_session_data(session_id, session_data)

        # Return the final, reflected answer.
        return {"botMessage": reflected_answer}
    except requests.RequestException as e:
        print("Error calling Cohere API:", e)
        raise HTTPException(status_code=500, detail="Failed to process the request")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from agents.transcription_agent import TranscriptionAgent
from agents.search_agent import SearchAgent
from agents.display_agent import DisplayAgent
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
transcription_agent = TranscriptionAgent()
search_agent = SearchAgent()
display_agent = DisplayAgent()

@app.websocket("/audio")
async def audio_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            audio_data = await websocket.receive_bytes()
            transcription = await transcription_agent.transcribe_audio(audio_data)

            if transcription:
                await websocket.send_text(f"📝 Transcribed Text: {transcription}")
                
                # Search Results Logic
                search_results = search_agent.get_results(transcription)

                # Display results
                if search_results:
                    await websocket.send_text(f"📋 Results: {search_results}")
                else:
                    await websocket.send_text("❌ No results found.")
            else:
                await websocket.send_text("❌ Error: No transcription detected.")
                
    except WebSocketDisconnect:
        print("WebSocket connection closed")
    except Exception as e:
        await websocket.send_text(f"❌ Error: {str(e)}")

# Test Route for Health Check
@app.get("/")
async def root():
    return {"message": "Server is running successfully!"}

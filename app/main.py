from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, notes, websocket

app = FastAPI(title="NoteFlow Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # For development. For security in production, use your deployed frontend URL, e.g. ["https://yourfrontend.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])

# Optionally, add a root endpoint to verify API health
@app.get("/")
async def root():
    return {"message": "Welcome to NoteFlow-backend!"}

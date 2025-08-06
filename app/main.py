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

app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(websocket.router)

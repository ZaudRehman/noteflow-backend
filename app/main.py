from fastapi import FastAPI
from app.routes import auth, notes, websocket

app = FastAPI(title="NoteFlow Backend")

app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(websocket.router)

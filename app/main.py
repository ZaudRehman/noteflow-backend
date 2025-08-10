from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, notes, websocket

app = FastAPI(title="NoteFlow Backend")

# CORS Middleware - Update allow_origins for production!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in prod, e.g. ["https://yourfrontend.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers without prefix in router files
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(websocket.router, tags=["websocket"])

@app.get("/")
async def root():
    return {"message": "Welcome to NoteFlow-backend!"}

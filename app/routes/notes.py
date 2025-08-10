from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Annotated
from app.models import insert_note, list_user_notes, get_note_by_id, update_note, delete_note_by_id
from app.utils.auth import get_current_user
from datetime import datetime

router = APIRouter(tags=["notes"])  

@router.post("/create")
async def create_note(
    title: Annotated[str, Body()],
    content: Annotated[str, Body()],
    current_user: Annotated[str, Depends(get_current_user)],
):
    note = {
        "title": title,
        "content": content,
        "collaborators": [current_user],
        "history": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    result = insert_note(note)
    return {"note_id": str(result.inserted_id)}

@router.get("/list")
async def notes_list(current_user: Annotated[str, Depends(get_current_user)]):
    notes = list_user_notes(current_user)
    # Convert ObjectIds to strings for frontend compatibility
    for note in notes:
        note["_id"] = str(note["_id"])
    return notes

@router.put("/update/{note_id}")
async def update_note_route(
    note_id: str,
    title: Annotated[str, Body()],
    content: Annotated[str, Body()],
    current_user: Annotated[str, Depends(get_current_user)],
):
    note = get_note_by_id(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    if current_user not in note["collaborators"]:
        raise HTTPException(status_code=403, detail="User not authorized to update this note")

    history_item = {
        "title": note["title"],
        "content": note["content"],
        "updated_at": note["updated_at"],
    }

    update_note(note_id, {
        "title": title,
        "content": content,
        "updated_at": datetime.utcnow(),
        "history": note.get("history", []) + [history_item], 
    })

    return {"message": "Note updated successfully"}

@router.delete("/delete/{note_id}")
async def delete_note_route(
    note_id: str,
    current_user: Annotated[str, Depends(get_current_user)],
):
    note = get_note_by_id(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    if note["collaborators"][0] != current_user:
        raise HTTPException(status_code=403, detail="Only the owner can delete this note")
    result = delete_note_by_id(note_id)
    if result.deleted_count == 1:
        return {"message": "Note deleted successfully"}
    raise HTTPException(status_code=500, detail="Note deletion failed")

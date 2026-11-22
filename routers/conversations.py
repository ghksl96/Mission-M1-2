from fastapi import APIRouter, HTTPException
from datetime import datetime
from database import db
from schemas import ConversationCreate

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])

@router.post("")
def save_conversation(conv: ConversationCreate):
    data = {
        "title": conv.title,
        "messages": conv.messages,
        "created_at": datetime.now().isoformat()
    }
    _, doc_ref = db.collection("conversations").add(data)
    return {"id": doc_ref.id, **data}

@router.get("")
def get_conversations():
    docs = db.collection("conversations").stream()
    result = [{"id": doc.id, **doc.to_dict()} for doc in docs]
    result.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return result

@router.get("/{conv_id}")
def get_conversation_detail(conv_id: str):
    doc = db.collection("conversations").document(conv_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다.")
    return {"id": doc.id, **doc.to_dict()}

@router.delete("/{conv_id}")
def delete_conversation(conv_id: str):
    doc_ref = db.collection("conversations").document(conv_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다.")
    doc_ref.delete()
    return {"message": "대화 삭제 완료", "id": conv_id}
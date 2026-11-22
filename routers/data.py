from fastapi import APIRouter, HTTPException
from database import db
from schemas import DataItem

router = APIRouter(prefix="/api/data", tags=["Data"])

def calculate_summary():
    docs = db.collection("data").stream()
    items = [doc.to_dict() for doc in docs]
    if not items:
        return {"count": 0, "message": "데이터가 없습니다."}

    items.sort(key=lambda x: x.get("date", ""))
    values = [float(x["value"]) for x in items]
    
    # 최근 추세 계산 (최근 7개 평균 vs 그 이전 7개 평균)
    trend = "유지"
    if len(values) >= 14:
        recent_avg = sum(values[-7:]) / 7
        prev_avg = sum(values[-14:-7]) / 7
        if recent_avg > prev_avg * 1.05:
            trend = "증가"
        elif recent_avg < prev_avg * 0.95:
            trend = "감소"

    return {
        "count": len(items),
        "period": f"{items[0]['date']} ~ {items[-1]['date']}",
        "average": round(sum(values) / len(values), 1),
        "max": max(values),
        "min": min(values),
        "trend": trend
    }

@router.get("/summary")
def get_summary():
    return calculate_summary()

@router.get("")
def get_all_data():
    docs = db.collection("data").stream()
    result = [{"id": doc.id, **doc.to_dict()} for doc in docs]
    result.sort(key=lambda x: x.get("date", ""), reverse=True)
    return result

@router.post("")
def create_data(item: DataItem):
    _, doc_ref = db.collection("data").add(item.model_dump())
    return {"id": doc_ref.id, **item.model_dump()}

@router.put("/{item_id}")
def update_data(item_id: str, item: DataItem):
    doc_ref = db.collection("data").document(item_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다.")
    doc_ref.update(item.model_dump())
    return {"id": item_id, **item.model_dump()}

@router.delete("/{item_id}")
def delete_data(item_id: str):
    doc_ref = db.collection("data").document(item_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다.")
    doc_ref.delete()
    return {"message": "삭제 완료", "id": item_id}
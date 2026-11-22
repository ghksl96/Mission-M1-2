import os
from datetime import datetime
import httpx
from fastapi import APIRouter, HTTPException
from database import db
from schemas import ChatRequest
from routers.data import calculate_summary

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("")
def chat_with_ai(req: ChatRequest):
    # 1. 현재 데이터 요약본 가져오기
    summary = calculate_summary()

    # 2. 시스템 프롬프트에 데이터 요약 주입
    system_prompt = f"""
    너는 사용자의 일일 학습 시간 데이터를 분석해 주는 친절한 AI 코치야.
    아래의 최신 데이터 요약 정보를 바탕으로 사용자의 질문에 구체적으로 답변해 줘.

    [현재 데이터 요약]
    - 기간: {summary.get('period')}
    - 총 데이터 개수: {summary.get('count')}개
    - 평균 학습 시간: {summary.get('average')}분
    - 최대/최소: {summary.get('max')}분 / {summary.get('min')}분
    - 최근 추세: {summary.get('trend')}
    """

    # 3. 기존 대화 불러오기
    messages = []
    if req.conversation_id:
        doc = db.collection("conversations").document(req.conversation_id).get()
        if doc.exists:
            messages = doc.to_dict().get("messages", [])

    messages.append({"role": "user", "content": req.message})

    # 4. Gemini 공식 API 직접 호출
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    contents = [
        {
            "role": "model" if m["role"] == "assistant" else "user",
            "parts": [{"text": m["content"]}]
        }
        for m in messages
    ]

    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": contents
    }

    try:
        res = httpx.post(url, json=payload, timeout=30.0)
        if res.status_code != 200:
            raise HTTPException(status_code=500, detail=f"AI 오류 ({res.status_code}): {res.text}")
        ai_reply = res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 오류: {str(e)}")

    messages.append({"role": "assistant", "content": ai_reply})

    # 5. 대화 내용 자동 저장
    if req.conversation_id:
        db.collection("conversations").document(req.conversation_id).update({
            "messages": messages
        })
        conv_id = req.conversation_id
    else:
        title = req.message[:20] + ("..." if len(req.message) > 20 else "")
        _, doc_ref = db.collection("conversations").add({
            "title": title,
            "messages": messages,
            "created_at": datetime.now().isoformat()
        })
        conv_id = doc_ref.id

    return {
        "reply": ai_reply,
        "conversation_id": conv_id,
        "summary_used": summary
    }
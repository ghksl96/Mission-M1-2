from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import data, conversations, chat

app = FastAPI(title="AI 데이터 분석 챗봇 API")

# 프론트엔드(Vercel 등)에서 백엔드로 요청을 보낼 수 있게 허용 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 분리해 둔 라우터 연결
app.include_router(data.router)
app.include_router(conversations.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "AI 데이터 분석 챗봇 백엔드 서버가 정상 작동 중입니다."}
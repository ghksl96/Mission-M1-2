# 📊 AI 학습 데이터 분석 챗봇 (Mission-M1-2)

일일 학습 시간 시계열 데이터(100개 이상)를 기록·관리(CRUD)하고, 저장된 최신 데이터 요약 정보를 AI 시스템 프롬프트에 자동 주입(컨텍스트 주입)하여 맞춤형 학습 피드백을 제공하는 풀스택 웹 애플리케이션입니다.

## 🌐 배포 주소
- **프론트엔드 (Vercel):** https://mission-m1-2-frontend-gamma.vercel.app
- **백엔드 API (Render):** https://mission-m1-2.onrender.com
- **API 문서 (Swagger UI):** https://mission-m1-2.onrender.com/docs

> ※ Render 무료 티어 특성상 일정 시간 미사용 후 첫 요청 시 서버가 깨어나는 데(콜드 스타트) 30초~1분 정도 소요될 수 있습니다.

## 🛠 기술 스택
- **Frontend:** HTML, CSS, Vanilla JavaScript (Vercel 배포)
- **Backend:** Python 3.10+, FastAPI, Uvicorn, Pydantic (Render 배포)
- **Database:** Firebase Firestore (`data`, `conversations` 컬렉션)
- **AI Model:** Google Gemini (`gemini-3.8-flash`, 공식 REST API 연동)

## ✨ 주요 기능
1. **학습 데이터 요약 대시보드:** 기간, 총 개수, 평균·최대·최소 학습 시간 및 최근 추세 자동 계산 (`GET /api/data/summary`)
2. **데이터 관리 (CRUD):** 학습 기록 추가, 목록 조회, 수정 및 삭제
3. **데이터 기반 AI 채팅:** 최신 데이터 요약을 시스템 프롬프트에 주입하여 답변 생성 및 로딩 표시
4. **대화 기록 관리:** Firestore에 대화 내역 자동 저장, 목록 조회 및 이전 대화 불러오기

## 💻 로컬 실행 방법

### 1) 백엔드 실행
```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 서버 실행 (실행 후 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 에서 Swagger 확인)
uvicorn main:app --reload
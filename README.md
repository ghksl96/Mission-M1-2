# 📊 AI 학습 데이터 분석 챗봇 (Mission-M1-2)

일일 학습 시간 데이터를 기록·관리(CRUD)하고, 저장된 최신 데이터를 바탕으로 AI 코치와 대화하며 학습 추세를 분석할 수 있는 풀스택 웹 애플리케이션입니다.

## 🌐 배포 주소
- **프론트엔드 (Vercel):** https://mission-m1-2-frontend-gamma.vercel.app
- **백엔드 API (Render):** https://mission-m1-2.onrender.com
- **API 문서 (Swagger):** https://mission-m1-2.onrender.com/docs

> ※ Render 무료 서버 특성상 일정 시간 미사용 후 첫 접속 시 서버가 깨어나는 데 30초~1분 정도 소요될 수 있습니다.

## 🛠 기술 스택
- **Frontend:** HTML, CSS, Vanilla JavaScript (Vercel 배포)
- **Backend:** Python, FastAPI, Uvicorn (Render 배포)
- **Database:** Firebase Firestore
- **AI Model:** Google Gemini (`gemini-3.8-flash`, 공식 REST API 연동)

## ✨ 주요 기능
1. **학습 데이터 요약 대시보드:** 기간, 총 데이터 개수, 평균·최대·최소 학습 시간 및 최근 추세 자동 계산
2. **데이터 관리 (CRUD):** 새로운 학습 기록 추가, 목록 조회 및 삭제
3. **데이터 기반 AI 채팅:** 최신 학습 데이터 요약본을 시스템 프롬프트에 자동 주입하여 맞춤형 피드백 제공
4. **대화 기록 관리:** Firestore에 대화 내역 자동 저장 및 이전 대화 이어하기 지원
# 📊 AI 학습 데이터 분석 챗봇 (Mission-M1-2)

일일 학습 시간 시계열 데이터(100개 이상)를 기록·관리(CRUD)하고, 저장된 최신 데이터 요약 정보를 AI 시스템 프롬프트에 자동 주입(컨텍스트 주입)하여 맞춤형 학습 피드백을 제공하는 풀스택 웹 애플리케이션입니다.

## 🌐 배포 주소 및 실행 확인
- **프론트엔드 (Vercel):** https://mission-m1-2-frontend-gamma.vercel.app
- **백엔드 API (Render):** https://mission-m1-2.onrender.com
- **API 문서 (Swagger UI):** https://mission-m1-2.onrender.com/docs

> ※ Render 무료 티어 특성상 일정 시간 미사용 후 첫 요청 시 서버가 깨어나는 데(콜드 스타트) 30초~1분 정도 소요될 수 있습니다.

## 🛠 기술 스택
- **Frontend:** HTML, CSS (반응형 미디어쿼리 적용), Vanilla JavaScript (Vercel 배포)
- **Backend:** Python 3.10+, FastAPI, Uvicorn, Pydantic (Render 배포)
- **Database:** Firebase Firestore (`data`, `conversations` 컬렉션)
- **AI Model:** Google Gemini (`gemini-3.8-flash`, 공식 REST API 연동)

---

## 🏗 아키텍처 및 설계 의도

### 1. Firestore 컬렉션 설계 근거 (`data` / `conversations`)
- **설계 구조:** 시계열 학습 기록을 저장하는 `data` 컬렉션과 AI 채팅 내역을 저장하는 `conversations` 컬렉션을 최상위 레벨에서 분리했습니다.
- **장점:** 학습 데이터 요약(`GET /api/data/summary`)과 대화 목록 조회(`GET /api/conversations`)의 조회 패턴과 생명주기가 다르므로, 컬렉션을 분리함으로써 불필요한 문서 읽기(Read) 비용을 줄이고 각 기능의 독립적인 확장이 가능합니다.
- **단점 및 고려사항:** 단일 문서 내 `messages` 배열로 대화를 저장하는 구조이므로, 대화가 극단적으로 길어질 경우 Firestore 문서 크기 제한(1MB)에 도달할 수 있어 추후 서브컬렉션(`messages`) 분리로 확장할 수 있도록 설계했습니다.

### 2. 요약 API (`GET /api/data/summary`) 분리 이유
- **책임 분리 및 재사용성:** 통계 계산(기간, 평균, 최대/최소, 최근 추세) 로직을 별도 엔드포인트와 함수(`calculate_summary`)로 분리했습니다.
- **재사용 시나리오:** 프론트엔드 상단 대시보드 UI 렌더링과 백엔드 AI 채팅(`POST /api/chat`)의 시스템 프롬프트 생성 양쪽에서 동일한 요약 로직을 재사용하여 데이터 일관성을 보장합니다.

### 3. 컨텍스트 주입(시스템 프롬프트)의 장단점
- **기대 효과:** 모델에 최신 학습 데이터 요약본을 직접 주입함으로써 환각(Hallucination)을 줄이고, 별도의 모델 파인튜닝 없이도 실시간으로 갱신된 수치 기반의 정확한 맞춤형 피드백을 제공할 수 있습니다.
- **잠재 리스크 및 대응:**
  - *토큰 비용 및 지연 시간 증가:* 원본 데이터 100개를 모두 넣지 않고 **요약 정보만 주입**하여 토큰 사용량과 응답 지연을 최소화했습니다.
  - *프롬프트 인젝션/보안 리스크:* Pydantic `Field` 및 `validator`를 통해 사용자 입력 길이와 형식을 제한하여 비정상적인 입력을 1차 방어했습니다.

### 4. 대화 저장 전략 (시점 및 포맷)
- **저장 시점:** 사용자가 메시지를 보내고 AI 모델의 응답이 정상적으로 생성된 직후(`POST /api/chat` 내부) Firestore에 **자동 저장**됩니다. (AI 호출 실패 시 불완전한 대화가 저장되지 않도록 방지)
- **저장 방식:** `conversation_id`가 없으면 첫 질문 앞 20자를 제목(`title`)으로 새 문서를 생성(`add`)하고, 기존 대화 ID가 있으면 해당 문서의 `messages` 배열을 갱신(`update`)합니다.
- **저장 포맷:** `{ title: string, messages: [{ role: "user"|"assistant", content: string }], created_at: ISO8601 }`

---

## 💻 로컬 실행 방법

1. 프론트엔드 배포 화면 (데이터 요약 + AI 채팅) <br>

 <img width="1908" height="783" alt="이미지1" src="https://github.com/user-attachments/assets/4c2a825c-dbda-46a8-9284-0e6be0470ad1" />
 <br><br>

 2. 백엔드 배포 확인 (Swagger UI) 

<img width="1226" height="848" alt="Screenshot_6" src="https://github.com/user-attachments/assets/b7611623-0c89-486f-a8c0-d9420b3d3d63" />
<br><br>

3. 데이터 관리 화면 (CRUD 동작) 

<img width="1874" height="699" alt="Screenshot_7" src="https://github.com/user-attachments/assets/60053754-f450-453f-a62e-771e859d0f1d" />

<br><br>

4. 대화 기록 화면 (이전 대화 불러오기) <br>

<img width="1893" height="611" alt="Screenshot_8" src="https://github.com/user-attachments/assets/ab1eead2-15aa-474a-bddb-843769588784" />

<br>




### 1) 백엔드 실행
```bash
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload



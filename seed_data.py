import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# 1. 환경변수 및 Firebase 연결
load_dotenv()
cred_path = os.getenv("FIREBASE_KEY_PATH", "firebase-key.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. 샘플 메모 목록
memos = [
    "파이썬 기초 복습", "FastAPI 라우터 공부", "알고리즘 문제 풀이",
    "프로젝트 기획서 작성", "컨디션 난조로 가볍게 복습", "집중 잘됨! 야간 자율학습",
    "주말 보충 학습", "API 연동 테스트", "프론트엔드 CSS 정리"
]

# 3. 100일 치 시계열 데이터 생성 및 업로드
start_date = datetime.now() - timedelta(days=100)
batch = db.batch()

print("데이터 100개를 Firestore에 넣는 중...")

for i in range(100):
    current_date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
    # 최근으로 올수록 공부 시간이 조금씩 늘어나는 추세 반영
    base_value = 60 + int(i * 0.8) + random.randint(-20, 30)
    value = max(10, base_value)
    memo = random.choice(memos)

    doc_ref = db.collection("data").document()
    batch.set(doc_ref, {
        "date": current_date,
        "value": value,
        "memo": memo
    })

batch.commit()
print("완료! Firestore 'data' 컬렉션에 100개의 데이터가 저장되었습니다.")
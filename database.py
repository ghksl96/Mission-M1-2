import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()

if not firebase_admin._apps:
    # 배포 환경(Render)에서는 환경변수에 JSON 문자열을 통째로 넣어 사용
    cred_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    if cred_json:
        cred = credentials.Certificate(json.loads(cred_json))
    else:
        # 내 컴퓨터(로컬)에서는 firebase-key.json 파일 사용
        cred_path = os.getenv("FIREBASE_KEY_PATH", "firebase-key.json")
        cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()
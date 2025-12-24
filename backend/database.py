from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite 파일 위치 (backend 폴더 내 상대 경로 유지)
DB_FILE = "daangn.db"
DATABASE_URL = f"sqlite:///./{DB_FILE}"

# FastAPI 다중 스레드 접근을 위해 check_same_thread=False 설정
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 모델들이 공유하는 Base
Base = declarative_base()


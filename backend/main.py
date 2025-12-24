from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import models
from database import Base, SessionLocal, engine
from schemas import RegionOut

# API 시작 시 테이블이 없으면 생성 (이미 있으면 건너뜀)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HoneyCarrot API",
    description="당근 꿀매물 분석기 - FastAPI 백엔드 초기 버전",
    version="0.1.0",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/regions", response_model=List[RegionOut])
def list_regions(limit: int = 20, db: Session = Depends(get_db)):
    """간단히 지역 데이터 샘플을 반환."""
    return (
        db.query(models.Region)
        .order_by(models.Region.id.asc())
        .limit(limit)
        .all()
    )


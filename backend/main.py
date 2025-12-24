from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

import models
from database import Base, SessionLocal, engine
from schemas import ItemSearchOut, RegionOut

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


@app.get("/regions/search", response_model=List[RegionOut])
def search_regions(q: str, limit: int = 20, db: Session = Depends(get_db)):
    """여러 토큰(공백 구분)이 모두 포함된 지역을 부분 일치로 검색"""
    keyword = q.strip()
    tokens = [t for t in keyword.split() if t]
    if not tokens:
        return []

    query = db.query(models.Region)
    for token in tokens:
        pattern = f"%{token}%"
        query = query.filter(
            or_(
                models.Region.full_name.ilike(pattern),
                models.Region.name1.ilike(pattern),
                models.Region.name2.ilike(pattern),
                models.Region.name3.ilike(pattern),
                models.Region.region_code.ilike(pattern),
            )
        )

    return query.order_by(models.Region.id.asc()).limit(limit).all()


@app.get("/items/search", response_model=List[ItemSearchOut])
def search_items(
    region_code: str,
    keyword: str,
    limit: int = 20,
):
    """당근 중고거래 검색 결과를 스크래핑해 반환"""
    region_id = region_code.split("-")[-1].strip()
    if not region_id or not keyword.strip():
        raise HTTPException(status_code=400, detail="region_code와 keyword를 입력하세요.")

    url = "https://www.daangn.com/kr/buy-sell/"
    headers = {
        "User-Agent": "HoneyCarrotBot/1.0 (+mailto:saraitne11@naver.com)",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    params = {"region_ids[]": region_id, "search": keyword}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10, verify=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"요청 실패: {e}")

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="당근 검색 실패")

    soup = BeautifulSoup(resp.text, "html.parser")
    items: List[ItemSearchOut] = []

    for article in soup.select("article[data-article-id]"):
        item_id = article.get("data-article-id")
        title_el = article.select_one(".article-title") or article.select_one(".card-title")
        price_el = article.select_one(".article-price") or article.select_one(".card-price")
        region_el = article.select_one(".article-region-name") or article.select_one(
            ".card-region-name"
        )
        img_el = article.select_one("img")
        link_el = article.select_one("a")

        href = link_el.get("href") if link_el else None
        item_url = urljoin("https://www.daangn.com", href) if href else None

        items.append(
            ItemSearchOut(
                id=item_id,
                title=title_el.get_text(strip=True) if title_el else None,
                price=price_el.get_text(strip=True) if price_el else None,
                region=region_el.get_text(strip=True) if region_el else None,
                image_url=img_el.get("src") if img_el else None,
                url=item_url,
            )
        )

        if len(items) >= limit:
            break

    return items


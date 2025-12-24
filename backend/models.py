from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Region(Base):
    """지역 정보 (CSV 파일 내용과 1:1 매핑)"""

    __tablename__ = "regions"

    # CSV: region_code (PK, 예: 상하동-1686)
    region_code = Column(String(50), primary_key=True)

    # CSV: id (숫자 ID)
    id = Column(Integer, nullable=False)

    # CSV: full_name (전체 주소)
    full_name = Column(String(100), nullable=False)

    # CSV: 주소 분리
    name1 = Column(String(50))  # 시/도
    name2 = Column(String(50))  # 시/군/구
    name3 = Column(String(50))  # 읍/면/동

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    items = relationship("Item", back_populates="region")


class Item(Base):
    """매물 정보"""

    __tablename__ = "items"

    id = Column(String(50), primary_key=True)
    region_code = Column(String(50), ForeignKey("regions.region_code"))

    title = Column(String(255), nullable=False)
    image_url = Column(Text)
    url = Column(Text, nullable=False)
    seller_name = Column(String(100))
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    region = relationship("Region", back_populates="items")
    prices = relationship(
        "PriceHistory", back_populates="item", cascade="all, delete-orphan"
    )


class PriceHistory(Base):
    """시세 기록"""

    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(String(50), ForeignKey("items.id"))
    price = Column(Integer, nullable=False)
    recorded_at = Column(DateTime, default=datetime.now)

    item = relationship("Item", back_populates="prices")


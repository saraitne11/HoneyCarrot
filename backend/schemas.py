from pydantic import BaseModel


class RegionOut(BaseModel):
    region_code: str
    id: int
    full_name: str
    name1: str | None = None
    name2: str | None = None
    name3: str | None = None

    class Config:
        orm_mode = True


class ItemSearchOut(BaseModel):
    id: str | None = None
    title: str | None = None
    price: str | None = None
    region: str | None = None
    image_url: str | None = None
    url: str | None = None

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


from pydantic import BaseModel

class SubSourceOut(BaseModel):
    id: int
    name: str
    source_id: int

    class Config:
        orm_mode = True

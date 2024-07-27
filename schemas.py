from pydantic import BaseModel

class MemeAdd(BaseModel):
    name: str

class MemeFind(MemeAdd):
    id: int
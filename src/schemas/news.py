from pydantic import BaseModel
from datetime import date
from typing import List

class NewBase(BaseModel):
    title: str
    body: str
    date: date


class NewCreate(NewBase):
    pass

class NewResponse(NewBase):
    id: int
    title: str
    body: str
    date: date
    images: List[dict]


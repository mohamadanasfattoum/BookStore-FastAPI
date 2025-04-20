
from pydantic import BaseModel
from typing import Optional

class BookCreateSchema(BaseModel):
    title: str
    description: str
    author_id: int


class BookResponseSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    author_id: int


class BookUpdateSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    author_id: Optional[int]
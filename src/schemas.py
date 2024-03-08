from pydantic import BaseModel
from typing import List



class Review(BaseModel):
    text_review: str
    rating: float


class BookBase(BaseModel):

    title: str
    author: str
    publication_year: int


class Book(BookBase):

    reviews: List[Review] = []
    class Config:
        orm_mode = True

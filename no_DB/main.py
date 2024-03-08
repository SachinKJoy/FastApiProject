from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Mock database
books_db = []


# text_review: Optional[str] = None

class Book(BaseModel):
    title: str
    author: str
    publication_year: int

class Review(BaseModel):
    text_review: str
    rating: float

app = FastAPI()



""" Adds a new book with given id """
@app.post("/books/{book_id}")
async def add_book(book_id: int, book: Book):

    print("Books Db :", books_db)
    
    if books_db:
        for books in books_db:
            if books.get("book_id") == book_id:    
                raise HTTPException(status_code=409, detail="Book Already Exists with the given Id")
    
    books_db.append({"book_id": book_id, **book.dict()})
    return { "message" : "Book Added Successfully"}



""" Adds a review to a book based on the id """
@app.post("/books/{book_id}/add_review")
async def add_review(book_id: int, review: Review):
    print("Books Db :", books_db)
    for book in books_db:
        if book.get("book_id") == book_id:
            if book.get("reviews"):
                book["reviews"].append(review.dict())
            else:
                book["reviews"] = [review.dict()]

            return book

    raise HTTPException(status_code=404, detail="Book not found")



""" Returns Books list based on author or publication year"""
@app.get("/books")
def get_books_by_author_or_year(author: Optional[str] = None, publication_year: Optional[int] = None):
    
    books = [book for book in books_db if (not author or book.get("author") == author) and\
                (not publication_year or book.get("publication_year") == publication_year)]
    if books:
        return books
    
    raise HTTPException(status_code=404, detail="Books not found")
    


""" Returns all the reviews for a particular book"""
@app.get("/books/{book_id}/reviews")
def get_reviews(book_id: int):
    for book in books_db:
        if book.get("book_id") == book_id:
            return book.get("reviews")
    
    raise HTTPException(status_code=404, detail="No reviews found for this book")

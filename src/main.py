from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)



app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



""" Adds a new book with a given id """
@app.post("/books/{book_id}")
def add_book(book_id: int, book: schemas.BookBase, db: Session = Depends(get_db)):

    db_book = crud.get_book_by_id(db, book_id=book_id)
    if db_book:
        raise HTTPException(status_code=400, detail="Book Already Exists with the given Id")
    return crud.create_book(db=db, book=book, book_id=book_id)



""" Adds a review to a book based on the book id """
@app.post("/books/{book_id}/add_review")
def add_review(book_id: int, review: schemas.Review, db: Session = Depends(get_db)):
    
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if db_book:
        return crud.create_review(db=db, review=review, book_id=book_id)
    raise HTTPException(status_code=400, detail="Book not found")




""" Returns Books list based on author or publication year"""
@app.get("/books")
def get_books_by_author_or_year(author: Optional[str] = None, publication_year: Optional[int] = None, db: Session = Depends(get_db)):

    if author and publication_year:
        return crud.get_books(db, author=author, publication_year=publication_year)

    elif author:
        return crud.get_books_by_author(db, author=author)
    
    elif publication_year:
        return crud.get_books_by_year(db, publication_year=publication_year)

    raise HTTPException(status_code=400, detail="Book not found")
    


""" Returns all the reviews for a particular book"""
@app.get("/books/{book_id}/reviews")
def get_reviews(book_id: int, db: Session = Depends(get_db)):
    db_review = crud.get_reviews_by_id(db, book_id=book_id)

    if db_review:
        return db_review
    
    raise HTTPException(status_code=404, detail="No reviews found for this book")


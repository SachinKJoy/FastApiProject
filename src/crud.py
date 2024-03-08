from sqlalchemy.orm import Session

import random
from datetime import datetime


from . import models, schemas


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.book_id == book_id).first()


def create_book(db: Session, book: schemas.BookBase, book_id: int):
    db_book = models.Book(**book.dict(), book_id=book_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def create_review(db: Session, review: schemas.Review, book_id: int):
    db_review = models.Review(**review.dict(),id = random.seed(datetime.now().timestamp()), book_id=book_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review 


def get_books(db: Session, author: str, publication_year: int):
    return db.query(models.Book).filter(
        models.Book.author == author,
        models.Book.publication_year == publication_year
    ).all()


def get_books_by_author(db: Session, author: str):
    return db.query(models.Book).filter(models.Book.author == author).all()


def get_books_by_year(db: Session, publication_year: int):
    return db.query(models.Book).filter(models.Book.publication_year == publication_year).all()


def get_reviews_by_id(db: Session, book_id: int):
    return db.query(models.Review).filter(models.Review.book_id == book_id).all()

# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# # def get_user_by_email(db: Session, email: str):
# #     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()





# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()



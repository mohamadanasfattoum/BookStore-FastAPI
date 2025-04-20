from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.book import Book
from schema.book import BookCreateSchema, BookResponseSchema


router= APIRouter(prefix="/api/books")








@router.post("/",response_model=BookResponseSchema) # out put schema
def create_books_api(book:BookCreateSchema, db:Session=Depends(get_db)): # join data
    db_book = Book(**book.model_dump()) # unpacking the data
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book




@router.get("/",response_model=List[BookResponseSchema]) # out put schema
def list_books_api(db:Session=Depends(get_db)):
    books = db.query(Book)
    return books 




@router.get("/{book_id}",response_model=BookResponseSchema) # out put schema
def book_detail_api(book_id:int , db:Session=Depends(get_db)): # join data
    book = db.query(Book).filter(Book.id==book_id).first()
    return book






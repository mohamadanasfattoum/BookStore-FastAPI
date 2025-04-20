from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from core.database import get_db
from models.book import Book
from schema.book import BookCreateSchema, BookResponseSchema, BookUpdateSchema

router= APIRouter(prefix="/api/books")








@router.post("/",response_model=BookResponseSchema) # out put schema
def create_books_api(book:BookCreateSchema, db:Session=Depends(get_db)): # join data
    db_book = Book(**book.model_dump()) # unpacking the data
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book




# @router.get("/",response_model=List[BookResponseSchema]) # out put schema
# def list_books_api(db:Session=Depends(get_db)):
#     books = db.query(Book)
#     return books 




@router.get("/{book_id}",response_model=BookResponseSchema) # out put schema
def book_detail_api(book_id:int , db:Session=Depends(get_db)): # join data
    book = db.query(Book).filter(Book.id==book_id).first()
    if not book:
        raise HTTPException(status_code=404,detail="Book not found")
    return book




@router.delete("/{book_id}",status_code=204) # out put schema
def delete_book_api(book_id:int , db:Session=Depends(get_db)): # join data
    book = db.query(Book).filter(Book.id==book_id).first()
    db.delete(book)
    db.commit()
    if not book:
        raise HTTPException(status_code=404,detail="Book not found")
    db.delete(book)
    db.commit()
    return {"detail":"book deleted successfully."}






@router.put("/{book_id}",response_model=BookResponseSchema) # out put schema
def update_books_api(book_id:int,book_update:BookUpdateSchema,db:Session=Depends(get_db)): # join data
    book = db.query(Book).filter(Book.id==book_id).first()
    if not book:
        raise HTTPException(status_code=404,detail="Book not found")

    update_data = book_update.model_dump() # unpacking the data
    for k, v in update_data.items():
        setattr(book, k, v) # update the data
    db.commit()
    db.refresh(book)
    return book



# search books
@router.get("/",response_model=List[BookResponseSchema]) # out put schema
def list_books_api(
    db:Session=Depends(get_db),
    search: Optional[str] = Query(None,description="Search by title or id"), # search query
    order_by: Optional[str] = Query("id",regex="^-?(title|id)$",description="Order y titleor description"), # order direction query

    ):
    books = db.query(Book)
    if search:
        books = books.filter(or_(Book.title.ilike(f"%{search}") | Book.description.ilike(f"%{search}%"))) # search by title or description

    if order_by == "title":
        books = books.order_by(Book.title) 
    elif order_by == "-title" or order_by == "-id":
        books = books.order_by(Book.title.desc())   
        
    return books
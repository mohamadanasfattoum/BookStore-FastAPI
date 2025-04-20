
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session


from core.database import get_db
from models.author import Author


router = APIRouter(prefix="/books")

@router.post("/create_author") # to insert authors in db 
def create_author(
    name:str = Form(...),
    db: Session = Depends(get_db)
):
    author = Author(name=name)
    db.add(author)
    db.commit()
    db.refresh(author)
    
    return author
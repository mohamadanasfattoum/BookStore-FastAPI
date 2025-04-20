from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


from core.database import get_db
from models.book import Book
from models.author import Author

# setup Router & template settings
router = APIRouter(prefix="/books")
templates = Jinja2Templates(directory="templates")



@router.get("/",include_in_schema=False)
def list_books(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book)
    return templates.TemplateResponse("books_list.html", {"request": request, "books": books})



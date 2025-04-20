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

@router.get("/create", include_in_schema=False)
def create_book_form(request: Request,db: Session = Depends(get_db)):
    authors = db.query(Author)
    return templates.TemplateResponse("books_create.html", {"request": request, "authors": authors})


@router.post("/", include_in_schema=False)
def create_book(
    title:str = Form(...),
    description:str = Form(...),
    author_id:int = Form(...),
    db: Session = Depends(get_db)
):
    book = Book(title=title, description=description, author_id=author_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return RedirectResponse(url="/books", status_code=303)

@router.get("/{book_id}", include_in_schema=False)
def book_detail(request: Request,book_id:int,db: Session = Depends(get_db)):
    book = db.query(Book).get(book_id)
    # book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("books_detail.html", {"request": request, "book": book})
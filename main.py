from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles

from core.database import engine, Base

from api.books import router as books_api_router

# intialize app
app = FastAPI()

# mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# add routers
app.include_router(books_api_router)

# @app.get("/")
# async def main():
#     return {"message": "Hello World"}  


# create database tebles (all tables in Base )
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)

# To run the FastAPI application, use the command:
# python main.py 

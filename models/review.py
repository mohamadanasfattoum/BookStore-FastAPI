from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    rating = Column(Integer)

    # Foreign key to the Book table
    book_id = Column(Integer, ForeignKey("books.id"))

    # Relationship to the Book model
    book = relationship("Book", back_populates="reviews") 
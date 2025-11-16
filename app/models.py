from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    reviews = relationship("Review", back_populates="user")


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)

    reviews = relationship("Review", back_populates="hotel")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)

    rating = Column(Float, nullable=False)
    text = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sentiment = Column(String, nullable=True)  # es: "positive", "negative", "neutral"

    user = relationship("User", back_populates="reviews")
    hotel = relationship("Hotel", back_populates="reviews")

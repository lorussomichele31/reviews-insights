from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import engine, Base, SessionLocal
from app import models
from app.schemas import ReviewCreate, ReviewOut
from app.ml import analyze_sentiment
from fastapi import HTTPException

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/reviews", response_model=ReviewOut)
def create_review(payload: ReviewCreate, db: Session = Depends(get_db)):
    sentiment = analyze_sentiment(payload.text)

    review = models.Review(
        user_id=payload.user_id,
        hotel_id=payload.hotel_id,
        rating=payload.rating,
        text=payload.text,
        sentiment=sentiment,
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review



@app.get("/hotels/{hotel_id}/analytics")
def get_hotel_analytics(hotel_id: int, db: Session = Depends(get_db)):
    from sqlalchemy import func

    avg_rating = db.query(func.avg(models.Review.rating)).filter(
        models.Review.hotel_id == hotel_id
    ).scalar()

    if avg_rating is None:
        raise HTTPException(status_code=404, detail="Hotel not found or no reviews")

    sentiment_counts = (
        db.query(models.Review.sentiment, func.count(models.Review.id))
        .filter(models.Review.hotel_id == hotel_id)
        .group_by(models.Review.sentiment)
        .all()
    )

    sentiment_dict = {s: c for s, c in sentiment_counts}

    return {
        "hotel_id": hotel_id,
        "average_rating": float(avg_rating),
        "sentiment_distribution": sentiment_dict,
    }
from pydantic import BaseModel

class ReviewCreate(BaseModel):
    user_id: int
    hotel_id: int
    rating: float
    text: str

class ReviewOut(BaseModel):
    id: int
    user_id: int
    hotel_id: int
    rating: float
    text: str
    sentiment: str

    class Config:
        orm_mode = True
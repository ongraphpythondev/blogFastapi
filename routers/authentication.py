from fastapi import APIRouter, Depends, HTTPException, status
import schemas, models
from sqlalchemy.orm import Session
from database import get_db
from hashing import Hash
from .token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags= ["Authentication"]
)

@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials!")
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Password!")

    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


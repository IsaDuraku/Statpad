from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import UserCreate, UserDB, UserInDB
from app.models.auth import Token, TokenData
from app.database import SessionLocal
from app.routers.security import create_access_token, get_password_hash, verify_password

router = APIRouter()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register/", response_model=UserInDB)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    

    user_dict = user.dict(exclude={"password"})
    
    user_db = UserDB(**user_dict, password=hashed_password)
    
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    
    return user_db

@router.post("/login/", response_model=Token)
def login_user(user_credentials: UserCreate, db: Session = Depends(get_db)):
    username = user_credentials.username
    password = user_credentials.password

    db_user = db.query(UserDB).filter(UserDB.username == username).first()
    if db_user is None or not verify_password(password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

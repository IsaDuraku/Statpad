from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.models.user import User, UserDB, UserInDB
from app.models.auth import Token
from app.database import SessionLocal
from app.routers.security import create_access_token, get_password_hash, verify_password, \
    generate_verification_token
import smtplib
from email.mime.text import MIMEText
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register/", response_model=UserInDB)
def register_user(user: User, db: Session = Depends(get_db)):
    if user.email is None:
        raise HTTPException(status_code=400, detail="Email is required for registration")

    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)

    user_dict = user.dict(exclude={"password"})
    verification_token = generate_verification_token()
    user_db = UserDB(**user_dict, password=hashed_password, verification_token=verification_token, is_verified=False)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    # Send the email with the verification link
    send_email(user.email, verification_token)

    return user_db


def send_email(email: str, verification_token: str):
    # Construct the verification link
    verification_link = f"http://localhost:8000/api/verify-email/?token={verification_token}"

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "teampython91@gmail.com"
    smtp_password = "seke onpu smgf aqem"

    msg = MIMEText(f"Click the following link to verify your email: {verification_link}")
    msg["Subject"] = "Email Verification"
    msg["From"] = "teampython91@gmail.com"
    msg["To"] = email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail("teampython91@gmail.com", [email], msg.as_string())
    except Exception as e:
        # Handle email sending errors here
        print("Email sending error:", str(e))


@router.post("/login/", response_model=Token)
def login_user(user_credentials: User, db: Session = Depends(get_db)):
    username = user_credentials.username
    password = user_credentials.password

    db_user = db.query(UserDB).filter(UserDB.username == username).first()
    if db_user is None or not verify_password(password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify-email/")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.verification_token == token).first()
    if user:
        user.is_verified = True
        user.verification_token = None  # Clear the token after verification
        db.commit()
        return {"message": "Email verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid token")


@router.get('/view')
async def highlights_view(request: Request):
    db: Session = SessionLocal()
    hg = db.query(UserDB).all()
    return templates.TemplateResponse('auth.html', {'request': request, 'hg': hg})



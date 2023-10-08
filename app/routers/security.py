from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from passlib.context import CryptContext
import secrets

# Secret key for token signing (keep this secret)
SECRET_KEY = "ede2ac3b38a9bdc5d90eb58c9e379f34cd18c8ffafa3b254c3879f15b8039f05"

# Algorithm to use for token signing
ALGORITHM = "HS256"

# Token expiration time (e.g., 15 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Function to create an access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Create a CryptContext instance for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



def generate_verification_token():
    return secrets.token_urlsafe(32)

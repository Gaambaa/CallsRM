from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.service import AuthService
from app.config import settings

# JWT configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class AuthController:
    @staticmethod
    def create_access_token(data: dict) -> str:
        # Creates a JWT token with an expiration time
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)

    @staticmethod
    async def register(session: AsyncSession, email: str, password: str):
        # Check if user already exists
        existing = await AuthService.get_user_by_email(session, email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        user = await AuthService.create_user(session, email, password)
        return {"message": "User created", "email": user.email}

    @staticmethod
    async def login(session: AsyncSession, email: str, password: str):
        # Verify credentials and return JWT token
        user = await AuthService.get_user_by_email(session, email)
        if not user or not AuthService.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = AuthController.create_access_token({"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}
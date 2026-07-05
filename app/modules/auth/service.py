from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from app.models import User

# CryptContext defines which hashing algorithm to use.
# bcrypt is the industry standard for password hashing —
# it's slow by design, making brute force attacks expensive.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        # Converts plain text password to a bcrypt hash before storing in DB
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # Compares plain text password against stored hash without revealing the hash
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str):
        # Looks up a user by email — used during login
        result = await session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @staticmethod
    async def create_user(session: AsyncSession, email: str, password: str):
        # Hashes the password before storing — never saves plain text
        hashed = AuthService.hash_password(password)
        user = User(email=email, hashed_password=hashed)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
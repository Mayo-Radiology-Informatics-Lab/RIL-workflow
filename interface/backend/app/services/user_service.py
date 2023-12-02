from app.schemas.user_schema import UserAuth
from app.models.user_model import User
from app.core.security import get_password_hash, verify_password 
from typing import Optional
from uuid import UUID
from app.schemas.user_schema import UserUpdate
from pymongo.errors import OperationFailure

class UserService:
    @staticmethod
    async def create_user(data: UserAuth):
        user = User(
            email=data.email,
            username=data.username,
            hashed_password=get_password_hash(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            disabled=data.disabled,
            superuser=data.superuser
        )
        await user.save()
        return user

    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email=email) or await UserService.get_user_by_username(email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_password=user.hashed_password):
            return None
        
        return user
        
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        return user
    
    @staticmethod
    async def get_user_by_username(email: str) -> Optional[User]:
        user = await User.find_one(User.username == email)
        return user
    
    @staticmethod
    async def get_user_by_id(user_id: UUID) -> Optional[User]:
        user = await User.find_one(User.user_id == user_id)
        return user
    
    @staticmethod
    async def update_user(id: UUID, data: UserUpdate) -> User:
        user = await User.find_one(User.user_id == id)
        if not user:
            raise OperationFailure("User not found")
        
        new_user_data = User(
            email=data.email,
            username=data.username,
            hashed_password=get_password_hash(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            disabled=data.disabled,
            superuser=data.superuser
        )
        await user.update({"$set": new_user_data.dict(exclude_unset=True)})
        return user
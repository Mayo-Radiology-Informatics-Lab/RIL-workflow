from fastapi import APIRouter, HTTPException, status
from app.schemas.user_schema import UserAuth, UserOut
from app.services.user_service import UserService
from pymongo.errors import DuplicateKeyError, OperationFailure
from app.api.deps.user_deps import get_current_user
from app.models.user_model import User
from app.schemas.user_schema import UserUpdate
from fastapi import Depends


user_router = APIRouter()

@user_router.post('/create', summary='Create a new user', response_model=UserOut)
async def create_user(data: UserAuth):
    try:
        return await UserService.create_user(data)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User already exists"
        )

@user_router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return user


@user_router.put('/update', summary='Update User', response_model=UserOut)
async def update_user(data: UserUpdate, user: User = Depends(get_current_user)):
    try:
        return await UserService.update_user(user.user_id, data)
    except OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )
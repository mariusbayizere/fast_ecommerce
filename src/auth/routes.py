from fastapi import APIRouter, status, Depends
from .schemas import Create_User_model, UserResponse, User_Login_Model
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import det_session
from .service import user_service
from fastapi.exceptions import HTTPException
from .utils import create_access_token, verify_password, decode_token
from datetime import timedelta
from fastapi.responses import JSONResponse


auth_router = APIRouter()
User_Service = user_service()

REFERESHED_TOKEN_EXPIRE_MINUTES = 2


@auth_router.post('/signup', response_model=UserResponse ,status_code= status.HTTP_201_CREATED) 
async def create_user(user_data: Create_User_model, session: AsyncSession = Depends(det_session))-> UserResponse: 
    email = user_data.email
    user_exist = await User_Service.check_user_exist(email, session)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email this {email} is already exist" 
        )
    new_user = await User_Service.create_user(user_data, session)
    return new_user



@auth_router.post('/login', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def login_user(user_data: User_Login_Model, session: AsyncSession = Depends(det_session))-> UserResponse:
    email = user_data.email
    password = user_data.password

    user = await User_Service.get_user_by_email(email, session)

    if user is not None:
        validate_password = verify_password(password, user.password)
        if validate_password:
            access_token = create_access_token(user_data={"email": user.email, "user_id": user.id})

            refresh_token = create_access_token(
                user_data={
                    "email": user.email, 
                    "user_id": user.id},
                    refresh=True,
                    expiry=timedelta(days=REFERESHED_TOKEN_EXPIRE_MINUTES)
                    )
            
            return JSONResponse(
                content={
                    "Message":"Login Successfully",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "User":{
                    "user": user.id,
                    "User Name":user.username,
                    "email": user.email,
                    "role": user.role
                    }
                },
                status_code=status.HTTP_200_OK
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found"
        )
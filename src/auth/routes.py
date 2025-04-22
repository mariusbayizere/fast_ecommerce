from fastapi import APIRouter, status, Depends
from .schemas import Create_User_model, UserResponse, User_Login_Model
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import det_session
from .service import user_service
from fastapi.exceptions import HTTPException
from .utils import create_access_token, verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse
from .dependencies import Refresh_token_Bearer, Access_token_Bearer, get_current_user
from datetime import datetime
from src.db.redis import set_token

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
            detail=f"User with email {email} is not found"
        )
    
@auth_router.post('/refresh_token', status_code=status.HTTP_200_OK)
async def refresh_token(token_data: dict = Depends(Refresh_token_Bearer())):
    """
    Generate a new access token using a valid refresh token.
    """
    print("Token Data:", token_data)
    timestamp = token_data['exp']
    if datetime.fromtimestamp(timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_data["user"]
        )
        return JSONResponse(
            content={
                "access_token": new_access_token
            },
            status_code=status.HTTP_200_OK
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired token",
    )


@auth_router.get('/me', status_code=status.HTTP_200_OK)
async def get_currents_user(user=Depends(get_current_user)):
    """
    Get the current user using the access token.
    """
    return user



@auth_router.get('/logout', status_code=status.HTTP_200_OK)
async def get_current_user(token: dict = Depends(Access_token_Bearer())):
    jti = token['jti']
    await set_token(jti)
    return JSONResponse(
        content={
            "message": "Logout Successfully"
        },
        status_code=status.HTTP_200_OK
    )

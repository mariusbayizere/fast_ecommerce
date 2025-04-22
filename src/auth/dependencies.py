from fastapi.security import HTTPBearer
from fastapi import Request, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from fastapi.exceptions import HTTPException
from src.db.main import det_session
from src.db.redis import get_token
from .service import user_service


User_Service = user_service()

class token_Bearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        """this function is used to initialize the token bearer
        and set the auto_error to True or False

        Args:
            auto_error (bool, optional): _description_. Defaults to True.
        """
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials = await super().__call__(request)
        token = credentials.credentials
        token_data = decode_token(token)
        if token_data is None:
            return None
        if not self.token_validate(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if 'jti' in token_data and await get_token(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or has been  revoked",
                    "Resultion": "please get new acces token",
                    "status": False
                },
                headers={"WWW-Authenticate": "Bearer"}
            )

        self.verify_token_data(token_data)
        return token_data


    def token_validate(self, token: str)-> bool:
        token_data = decode_token(token)
        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError("This method is not implemented yet")
    

class Access_token_Bearer(token_Bearer):
    def verify_token_data(self, token_data: dict) -> None:
        """this function is used to verify the token data
        and check if the token is refresh token or not
        if the token is refresh token then it will raise HTTPException
        with status code 403 and detail message "please provide valid access token"

        Args:
            token_data (dict): token data

        Raises:
            HTTPException: if the token is refresh token
        """
        if token_data  and  token_data.get('refresh'):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="please provide valid access token",
                headers={"WWW-Authenticate": "Bearer"}
            )

class Refresh_token_Bearer(token_Bearer):
    def verify_token_data(self, token_data: dict) -> None:
        """This function is used to verify the token data
        and check if the token is refresh token or not
        if the token is not refresh token then it will raise HTTPException

        Args:
            token_data (dict): token data

        Raises:
            HTTPException: _description_: if the token is not refresh token
        403: _description_: Forbidden
        """
        if token_data and not token_data.get('refresh'):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="please provide valid refresh token",
                headers={"WWW-Authenticate": "Bearer"}
            )

async def get_current_user(token_data=Depends(Access_token_Bearer()), session: AsyncSession = Depends(det_session)):
    """This function is used to get the current user"""
    user_model = token_data["user"]["email"]
    user = await User_Service.get_user_by_email(user_model, session)
    return user
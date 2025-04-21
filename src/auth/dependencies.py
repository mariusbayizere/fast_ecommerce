from fastapi.security import HTTPBearer
from fastapi import Request, status
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from fastapi.exceptions import HTTPException

class token_Bearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
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
        self.verify_token_data(token_data)
        return token_data
            

    def token_validate(self, token: str)-> bool:
        token_data = decode_token(token)
        return True if token_data is not None else False

class Access_token_Bearer(token_Bearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data  and  token_data.get('refresh'):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="please provide valid access token",
                headers={"WWW-Authenticate": "Bearer"}
            )

class Refresh_token_Bearer(token_Bearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data.get('refresh'):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="please provide valid refresh token",
                headers={"WWW-Authenticate": "Bearer"}
            )


    
    def verify_token_data(self, token_data):
        raise NotImplementedError("This method is not implemented yet")
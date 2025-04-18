from fastapi import APIRouter, status 


auth_router = APIRouter()


@auth_router.post('/signup', status_code= status.HTTP_201_CREATED) 
async def create_user(): 
    pass   
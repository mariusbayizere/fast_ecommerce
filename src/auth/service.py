from sqlmodel.ext.asyncio.session import AsyncSession
from .models import User 
from sqlmodel import select
from src.auth.utils import generate_password_hash
from src.auth.schemas import Create_User_model


class user_service:

    async def get_user_by_email(self, email: str, session : AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user if user is not None else None
    

    async def check_user_exist(self, email: str, session : AsyncSession):
        user = await self.get_user_by_email(email, session)
        return True if user is not None  else False
    

    async def create_user(self, user_data: Create_User_model, session:AsyncSession):
        user_information = user_data.model_dump()
        new_user = User(
            **user_information
        )
        new_user.password = generate_password_hash(user_information['password'])
        session.add(new_user)
        await session.commit()
        return new_user
from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
from src.config import Config
import uuid

passwrd_context = CryptContext(
    schemes=["bcrypt"]
    )
ACCESS_TOKEN_EXPIRE_MINUTES = 3600

def generate_password_hash(password: str) -> str:
    """
    Generate a password hash using bcrypt.
    """
    return passwrd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return passwrd_context.verify(plain_password, hashed_password)


def create_access_token(user_data: dict, expiry : timedelta = None, refresh: bool = False) -> str:
    playload ={

    }
    playload['user'] = user_data
    playload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES))
    playload['jti'] = str(uuid.uuid4())
    # playload['iat'] = datetime.now()
    playload['refresh'] = refresh

    token_key = jwt.encode(
        payload=playload,
        key=Config.JWT_SECRETE,
        algorithm=Config.JWT_ALGORITHM
    )
    return token_key



def decode_token(token: str) -> dict:
    """
    Decode a JWT token and return the payload.
    """
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRETE,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}










def create_token(user_data: dict, expiry : timedelta = None) -> str:
    playload ={

    }
    playload['user'] = user_data
    playload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES))
    playload['jti'] = str(uuid.uuid4())
    # playload['iat'] = datetime.now()

    token_key = jwt.encode(
        playload=playload,
        key=Config.JWT_SECRETE,
        algorithm=Config.JWT_ALGORITHM
    )
    return token_key
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import settings
from schemas.other_schemas import Token


SERVER_KEY = settings.secret_key
ALGORITHM = settings.algorithm


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

# encode token function


def generate_token(user_id: int, email: str, activated: bool):
    payload = {"user_id": user_id, "email": email, "activated": activated}
    encoded_jwt = jwt.encode(payload, SERVER_KEY, algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer")

# decode token function


def decode_token_id(provided_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(provided_token, SERVER_KEY,
                             algorithms=[ALGORITHM])
        decoded_id: str = payload.get("user_id")
        decoded_email: str = payload.get("email")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return decoded_id


def decode_token_email(provided_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(provided_token, SERVER_KEY,
                             algorithms=[ALGORITHM])
        decoded_email: str = payload.get("email")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return decoded_email


def decode_token_status(provided_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(provided_token, SERVER_KEY,
                             algorithms=[ALGORITHM])
        decoded_email: str = payload.get("activated")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return decoded_email

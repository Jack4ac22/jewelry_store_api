import time
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
    expiration = time.time() + settings.expiration_minutes * 60
    payload = {"user_id": user_id, "email": email,
               "activated": activated, "expiration": expiration}
    encoded_jwt = jwt.encode(payload, SERVER_KEY, algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer")


def generate_validation_token(user_id: int, email: str, random_text: str, minutes: int = 43200):
    expiration = time.time() + minutes * 60
    payload = {"user_id": user_id, "email": email,
               "token": random_text, "expiration": expiration}
    encoded_jwt = jwt.encode(payload, SERVER_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# decode token function


def decode_token_id(provided_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(provided_token, SERVER_KEY,
                             algorithms=[ALGORITHM])
        decoded_id: str = payload.get("user_id")
        decoded_time: str = payload.get("expiration")
        if decoded_time < time.time():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Th token is expired.",
                headers={"WWW-Authenticate": "Bearer"}
            )
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


##### decode email for validation #####
def decode_token_email_validation(provided_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(provided_token, SERVER_KEY,
                             algorithms=[ALGORITHM])
        decoded_email: str = payload.get("email")
        decoded_time: str = payload.get("expiration")
        if decoded_time < time.time():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The Token was expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The token is invalid. please use the sent link without modification."
        )
    return decoded_email

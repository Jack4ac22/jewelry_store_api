from time import time
from sqlalchemy.orm.session import Session
from schemas import user_schemas, other_schemas
from .models import DbUser
from utilities import hash_manager, jwt_manager, email_manager
from db import db_check_methods
from fastapi import HTTPException, status
from pydantic import EmailStr
from config import settings


def create_user(request: user_schemas.UserBase, db: Session):
    db_check_methods.check_email_usage(request.email, db)
    hashed_password = hash_manager.hash_pass(request.password)
    generated_token = jwt_manager.generate_validation_token(
        time(), request.email, "ActivateMyAccount", 360)
    # print(generated_token)
    new_user = DbUser(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password=hashed_password,
        token=generated_token
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    email_manager.send_email_with_subject("API regestration.", request.email, "Verfication link", f"""Hello {request.first_name} {request.last_name},
    Please use the following link to verify your account
    {settings.host_name}/user/activate/{generated_token}
    This token is valid for 24 hrs only.
    Thank you.""")
    return new_user


def validate_email_address_for_new_user(token: str, db: Session):
    decoded_email = jwt_manager.decode_token_email_validation(token)
    targeted_user = db_check_methods.check_user_by_email(decoded_email, db)
    if targeted_user.first().token != token:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="The token is already used. please request a new token or contact support."
        )
    else:
        targeted_user.first().verified = True
        targeted_user.first().activated = True
        targeted_user.first().token = None
        db.commit()
        return targeted_user.first()

# TODO: add to the process the security questions which can be in another table, then answers should come in the request, after verification the process is done.
# TODO: possibly add a second solution which will require answering a question about the last order or any other personal data befor determining the fake trial.
# TODO: does not allow the request till one security question is answered. check what kind of schemas is there !!!


def reset_request(request: user_schemas.RequestPassword, db: Session):
    targeted_user = db_check_methods.check_user_by_email(request.email, db)
    generated_token = jwt_manager.generate_validation_token(
        time(), request.email, "Reset my password", 60)
    targeted_user.first().token = generated_token
    db.commit()
    email_manager.send_email_with_subject("password reset", request.email, "Verfication link", f"""Hello {targeted_user.first().first_name} {targeted_user.first().last_name},
    Please use the following link to resete your password.
    {settings.host_name}/user/activate/{generated_token}
    This link is valid for 1 hours.
    Thank you.""")
    return "The request is successfully done, please check your email and follow the instruction."


def reset_password_for_user(token: str, request: user_schemas.PasswordReset, db: Session):
    decoded_email = jwt_manager.decode_token_email_validation(token)
    targeted_user = db_check_methods.check_user_by_email(decoded_email, db)
    if targeted_user.first().token != token:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="The token is already used. please request a new token or contact support."
        )
    else:
        hashed_password = hash_manager.hash_pass(request.new_password)
        targeted_user.first().password = hashed_password
        targeted_user.first().token = None
        db.commit()
        return targeted_user.first()


def request_deactivation(id: int, db: Session):
    targeted_user = db_check_methods.check_user_id(id, db)
    generated_token = jwt_manager.generate_validation_token(
        id, targeted_user.first().email, targeted_user.first().activated, 60)
    targeted_user.first().token = generated_token
    db.commit()
    email_manager.send_email_with_subject("The Website", targeted_user.first().email, "deactivation request", f"""Hello {targeted_user.first().first_name} {targeted_user.first().last_name},
    Please use the following link to deactivate your account.
    {settings.host_name}/user/deactivate/{generated_token}
    This link is valid for 1 hours.
    Thank you.""")
    return f"A disactivation request has been sent, please check your email: {targeted_user.first().email} and follow the instruction."


def deactivate(token: other_schemas.Token, id: int, db: Session):
    targeted_user = db_check_methods.check_user_id(id, db)
    if targeted_user.first().token != token:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="The token is already used. please request a new token or contact support."
        )
    decoded_email = jwt_manager.decode_token_email_validation(token)
    targeted_user.first().token = None
    targeted_user.first().activated = False
    db.commit()
    return targeted_user.first()

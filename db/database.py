from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}'


database_engine = create_engine(DATABASE_URL)

SessionTemplate = sessionmaker(
    autocommit=False, autoflush=False, bind=database_engine)


def get_db():
    db = SessionTemplate()
    try:
        yield db
    finally:
        db.close()

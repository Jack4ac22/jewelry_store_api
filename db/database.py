from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}'
# DATABASE_URL = "mysql://root:root@localhost:8888/apidb"


database_engine = create_engine(DATABASE_URL)
db = database_engine.connect()
SessionTemplate = sessionmaker(
    autocommit=False, autoflush=False, bind=database_engine)


def get_db():
    db = SessionTemplate()
    try:
        yield db
    finally:
        db.close()

# def get_db():
#     db = database_engine.connect()
#     try:
#         yield db
#     finally:
#         db.close()

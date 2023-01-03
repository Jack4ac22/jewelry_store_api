from schemas import personalized_enums
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum, Float, Date, DateTime, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import enum

Base = declarative_base()


class DbUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        onupdate=func.current_timestamp(), nullable=True)
    activated = Column(Boolean, nullable=False, server_default="false")
    verified = Column(Boolean, nullable=False, server_default="false")
    token = Column(String, nullable=True)
    addresses = relationship("DbAddress", back_populates="user")


class DbAddress(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    address_description = Column(String, nullable=True)
    country = Column(String, nullable=False)
    state = Column(String, nullable=False)
    county = Column(String, nullable=False)
    street_name = Column(String, nullable=False)
    number = Column(String, nullable=False)
    extra_details = Column(String, nullable=True)
    active_address = Column(Boolean, server_default="false")

    user = relationship("DbUser", back_populates="addresses")


# class DbPerson(Base):
#     __tablename__ = 'person'
#     id = Column(Integer, primary_key=True, index=True)
#     first_name = Column(String, nullable=False)
#     last_name = Column(String, nullable=False)
#     gender = Column(Enum(personalized_enums.Genders_person), nullable=False)
#     email = Column(String, nullable=False, unique=True, index=True)
#     birthday = Column(Date, nullable=True, server_default="1900-01-31")
#     created_at = Column(TIMESTAMP(timezone=True),
#                         server_default=text('now()'), nullable=False)
#     updated_at = Column(TIMESTAMP(timezone=True),
#                         onupdate=func.current_timestamp(), nullable=True)
#     added_by = Column(Integer, ForeignKey(
#         "user.id", ondelete="CASCADE"), nullable=False)
#     user = relationship("DbUser")
#     phones = relationship("DbPhone", back_populates='person')
#     comments = relationship("DbComment", back_populates='person')
#     tasks = relationship("DbTask", back_populates='person')
#     job_titles = relationship("DbPersonJob", back_populates="person")


# class DbPhone(Base):
#     __tablename__ = 'phone'
#     id = Column(Integer, primary_key=True, index=True)
#     person_id = Column(Integer, ForeignKey(
#         "person.id", ondelete="CASCADE"), nullable=False)
#     phone = Column(String, nullable=False, unique=True, index=True)
#     description = Column(String, nullable=False,
#                          server_default="personal")
#     created_at = Column(TIMESTAMP(timezone=True),
#                         server_default=text('now()'), nullable=False)
#     updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(),
#                         onupdate=func.current_timestamp(), nullable=True)
#     person = relationship("DbPerson", back_populates='phones')
#     # TODO: added_by = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)


# class DbComment(Base):
#     __tablename__ = 'comment'
#     id = Column(Integer, primary_key=True, index=True)
#     person_id = Column(Integer, ForeignKey(
#         "person.id", ondelete="CASCADE"), nullable=False)
#     title = Column(String, nullable=True, unique=False)
#     content = Column(TEXT, nullable=True, unique=False)
#     created_at = Column(TIMESTAMP(timezone=True),
#                         server_default=text('now()'), nullable=False)
#     updated_at = Column(TIMESTAMP(timezone=True),
#                         onupdate=text('now()'), nullable=True)
#     person = relationship("DbPerson", back_populates='comments')
#     # TODO: added_by = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)


# class DbTask(Base):
#     __tablename__ = 'task'
#     id = Column(Integer, primary_key=True, index=True)
#     person_id = Column(Integer, ForeignKey(
#         "person.id", ondelete="CASCADE"), nullable=False)
#     title = Column(String, nullable=True)
#     content = Column(TEXT, nullable=True)
#     task_status = Column(Enum(personalized_enums.Task_status),
#                          nullable=False, server_default="task_open")
#     created_at = Column(TIMESTAMP(timezone=True),
#                         server_default=text('now()'), nullable=False)
#     updated_at = Column(TIMESTAMP(timezone=True),
#                         onupdate=func.current_timestamp(), nullable=True)
#     person = relationship("DbPerson", back_populates='tasks')
#     # TODO: added_by = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)


# class DbJobTitle(Base):
#     __tablename__ = 'job_title'
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     description = Column(String, nullable=True)
#     created_at = Column(TIMESTAMP(timezone=True),
#                         server_default=text('now()'), nullable=False)
#     updated_at = Column(TIMESTAMP(timezone=True),
#                         onupdate=func.current_timestamp(), nullable=True)
#     people = relationship("DbPersonJob", back_populates="job_title")


# class DbPersonJob(Base):
#     __tablename__ = 'person_job_title'
#     id = Column(Integer, primary_key=True, index=True)
#     person_id = Column(Integer, ForeignKey(
#         "person.id", ondelete="CASCADE"), nullable=False)
#     title_id = Column(Integer, ForeignKey(
#         "job_title.id", ondelete="CASCADE"), nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True),
#                         server_default=text('now()'), nullable=False)
#     updated_at = Column(TIMESTAMP(timezone=True),
#                         onupdate=func.current_timestamp(), nullable=True)
#     person = relationship("DbPerson", back_populates='job_titles')
#     job_title = relationship("DbJobTitle", back_populates='people')

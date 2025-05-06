from sqlalchemy import Column , String , Integer 
from src.core.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer , primary_key=True)
    username = Column(String , nullable=False)
    password = Column(String , nullable=False)
    role = Column(String , nullable=False)
    
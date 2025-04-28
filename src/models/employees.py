from sqlalchemy import Column , String , Integer , Boolean
from src.core.base import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer , primary_key=True)
    diplom = Column(String , nullable=False)
    passport = Column(String , nullable=False)
    resume = Column(String , nullable=False)
    phone_number = Column(String , nullable=False)
    is_read = Column(Boolean , nullable=False , default=False)
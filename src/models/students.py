from sqlalchemy import Column , String , Integer , Boolean
from src.core.base import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer , primary_key=True)
    first_name = Column(String , nullable=False)
    direction = Column(String , nullable=False)
    phone_number = Column(String , nullable=False)
    is_read = Column(Boolean , nullable=False , default=False)